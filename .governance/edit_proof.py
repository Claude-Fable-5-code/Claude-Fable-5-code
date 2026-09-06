#!/usr/bin/env python3
"""
edit_proof.py — "I edited X" is a claim about a diff, proven by the diff (R86, Round 13, Rule 31).

Usage:
    python .governance/edit_proof.py show <path> [<path>…]    # print an edit-proof block per path (run via attest.py)
    python .governance/edit_proof.py show <path> --scope A-B   # + every diff hunk must sit inside HEAD lines A..B (R92, Rule 37)
    python .governance/edit_proof.py check <turn.md>          # exit 1 if prose claims an edit with no matching proof
    python .governance/edit_proof.py --self-test

Why this exists (Round 13, RECONSTRUCTED after reset). The agent wrote "عدّلت intent_gate.py" / "fixed the
regex in claim_check.py" while the file on disk was unchanged, or changed differently than described.
Rule 18/25 already covers "updated on remote"; nothing covered "edited locally". This tool does:

  show   → for each path emit
              edit_proof <path>: <state> sha256=<12>
                +<added> -<removed>  (vs HEAD)              when the working tree differs from HEAD
                committed <7> <subject>                       when the tree == HEAD and HEAD touched the path
                head=<7>
              ✅ edit_proof: <path> <state>
           state ∈ {MODIFIED, STAGED, COMMITTED-IN-HEAD, UNTRACKED, UNCHANGED}. UNCHANGED means: the tree equals
           HEAD and HEAD did not touch the path — i.e. nothing was edited. Run under attest.py (Rule 21).

  check  → scan PROSE for EDIT verbs ("edited", "fixed", "patched", "changed", "rewrote", "عدّلت", "عدلت",
           "أصلحت", "صلحت", "غيّرت", "غيرت", "ضفت", "أضفت", "added … to") followed within the sentence by a file
           path. Each such path needs an edit_proof block in the same turn with state ≠ UNCHANGED whose sha256
           matches the file on disk now. Otherwise exit 1 and print the unproven claim.

  --scope A-B (Round 14, R92, Rule 37). The guide promised "edit only lines A-B" could be proven; the tool read
           `git diff --numstat` and could not see WHERE a change landed. Now `show` parses `git diff -U0 HEAD`
           hunks. A hunk `@@ -a,b +c,d @@` touches HEAD lines a..a+b-1 (b=0: pure insertion after line a).
           Every hunk must lie inside [A,B] (insertion: A-1 ≤ a ≤ B). One hunk outside ⇒
             ⛔ edit_proof: <path> OUT-OF-SCOPE  … exit 1.  Scope is HEAD numbering, so it is what the human read.
"""
import hashlib, pathlib, re, subprocess, sys

GOV = pathlib.Path(__file__).resolve().parent
ROOT = GOV.parent
sys.path.insert(0, str(GOV))
from claim_check import prose_and_blocks  # noqa: E402

EDIT = re.compile(r"\b(edited|fixed|patched|changed|rewrote|refactored|added|updated locally|modified)\b|عدّلت|عدلت|أصلحت|اصلحت|صلحت|غيّرت|غيرت|ضفت|أضفت|اضفت", re.I)
PATHISH = re.compile(r"(?<![\w/])((?:[\w.-]+/)*[\w.-]+\.(?:py|js|ts|tsx|jsx|sh|yml|yaml|json|md|toml|ini|cfg|ps1|txt))\b", re.I)
HDR = re.compile(r"^edit_proof (\S+): (MODIFIED|STAGED|COMMITTED-IN-HEAD|UNTRACKED|UNCHANGED) sha256=([0-9a-f]{12})$")


def sha12(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12] if p.exists() else "000000000000"


def git(*a) -> str:
    p = subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    return (p.stdout or "").strip()


def show_one(path: str):
    p = ROOT / path
    head = git("rev-parse", "--short=7", "HEAD") or "0000000"
    tracked = git("ls-files", "--error-unmatch", path) != "" if p.exists() else bool(git("ls-files", path))
    stat_wt = git("diff", "--numstat", "HEAD", "--", path)
    if stat_wt and stat_wt.split("\t")[:2] == ["0", "0"]:
        stat_wt = ""  # mode-only change (chmod) is not an edit
    stat_idx = git("diff", "--numstat", "--cached", "--", path)
    in_head = git("log", "-1", "--format=%h %s", "HEAD", "--", path)
    head_touched = bool(in_head) and git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD", "--", path) != ""
    if not tracked:
        state = "UNTRACKED"
    elif stat_wt:
        state = "STAGED" if stat_idx and not git("diff", "--numstat", "--", path) else "MODIFIED"
    elif head_touched:
        state = "COMMITTED-IN-HEAD"
    else:
        state = "UNCHANGED"
    out = [f"edit_proof {path}: {state} sha256={sha12(p)}"]
    if stat_wt:
        a, r, _ = stat_wt.split("\t", 2)
        out.append(f"  +{a} -{r}  (vs HEAD)")
    if state == "COMMITTED-IN-HEAD":
        out.append(f"  committed {in_head}")
    out.append(f"  head={head}")
    out.append(f"✅ edit_proof: {path} {state}" if state != "UNCHANGED" else f"⛔ edit_proof: {path} UNCHANGED — nothing was edited")
    return out, state


HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def hunks(path: str):
    """[(old_start, old_len, new_start, new_len)] from `git diff -U0 HEAD -- path` (index+tree vs HEAD)."""
    out = []
    for ln in git("diff", "-U0", "HEAD", "--", path).splitlines():
        m = HUNK.match(ln)
        if m:
            a, b, c, d = (int(x) if x is not None else 1 for x in m.groups())
            out.append((a, b, c, d))
    return out


def in_scope(h, lo: int, hi: int) -> bool:
    a, b, _, _ = h
    if b == 0:  # pure insertion after HEAD line a
        return lo - 1 <= a <= hi
    return lo <= a and a + b - 1 <= hi


def scope_lines(path: str, lo: int, hi: int):
    """Extra block lines + verdict for --scope. Returns (lines, ok)."""
    if not git("ls-files", "--error-unmatch", path):
        return [f"  scope {lo}-{hi}: file not in HEAD — scope cannot apply"], False
    hs = hunks(path)
    if not hs:
        return [f"  scope {lo}-{hi}: 0 hunk(s)"], True
    lines, bad = [f"  scope {lo}-{hi}: {len(hs)} hunk(s)"], 0
    for h in hs:
        ok = in_scope(h, lo, hi)
        bad += not ok
        lines.append(f"  @@ -{h[0]},{h[1]} +{h[2]},{h[3]} @@ {'in-scope' if ok else 'OUT-OF-SCOPE'}")
    return lines, bad == 0


def parse_scope(argv):
    """Strip `--scope A-B` from argv; return (paths, (A,B) | None). Malformed ⇒ SystemExit(2)."""
    if "--scope" not in argv:
        return argv, None
    i = argv.index("--scope")
    m = re.fullmatch(r"(\d+)-(\d+)", argv[i + 1] if i + 1 < len(argv) else "")
    if not m or int(m.group(1)) < 1 or int(m.group(1)) > int(m.group(2)):
        print("⛔ edit_proof: --scope needs A-B with 1 ≤ A ≤ B"); raise SystemExit(2)
    return argv[:i] + argv[i + 2:], (int(m.group(1)), int(m.group(2)))


def show(paths, scope=None) -> int:
    rc = 0
    for path in paths:
        out, state = show_one(path)
        if scope is not None:
            extra, ok = scope_lines(path, *scope)
            out[-1:-1] = extra  # before the verdict line
            if not ok:
                out[-1] = f"⛔ edit_proof: {path} OUT-OF-SCOPE — a hunk landed outside lines {scope[0]}-{scope[1]} (Rule 37)"
                rc |= 1
        print("\n".join(out))
        rc |= int(state == "UNCHANGED")
    return rc


def claims_in(prose: str):
    for s in re.split(r"(?<=[.!?؟])\s+|\n+", prose):
        if EDIT.search(s):
            for m in PATHISH.finditer(s):
                yield s.strip(), m.group(1)


def proofs_in(bl):
    out = {}
    for tool, rc, body in bl:
        if tool != "edit_proof":
            continue
        for ln in body:
            m = HDR.match(ln.strip())
            if m:
                out[m.group(1)] = (m.group(2), m.group(3))
    return out


def check_text(text: str, live=True):
    prose, bl = prose_and_blocks(text)
    proofs = proofs_in(bl)
    problems, claims = [], 0
    for sent, path in claims_in(prose):
        claims += 1
        key = next((k for k in proofs if k == path or k.endswith("/" + path) or path.endswith("/" + k)), None)
        if key is None:
            problems.append(f"no edit_proof for {path} — «{sent[:100]}»"); continue
        state, sha = proofs[key]
        if state == "UNCHANGED":
            problems.append(f"{path} proof says UNCHANGED — the edit did not happen"); continue
        if live and (ROOT / key).exists() and sha12(ROOT / key) != sha:
            problems.append(f"{path} proof sha {sha} ≠ disk {sha12(ROOT / key)} — stale proof")
    return problems, claims, len(proofs)


def check(path: str) -> int:
    text = pathlib.Path(path).read_text(encoding="utf-8")
    problems, n, np_ = check_text(text)
    print(f"edit_proof {path}: {n} edit claim(s), {np_} proof block(s)")
    for p in problems:
        print(f"🔴 {p}")
    if n == 0:
        print("ℹ️  edit_proof: no edit claim in this turn — nothing to prove"); return 0
    if problems:
        print(f"⛔ edit_proof: {len(problems)} claim(s) without a live diff — an edit you cannot show did not happen (Rule 31)"); return 1
    print("✅ edit_proof: every edit claim has a live proof"); return 0


def self_test() -> int:
    ok = True
    me = ".governance/edit_proof.py"
    out, state = show_one(me)
    ok &= out[0].startswith("edit_proof ") and state in ("UNTRACKED", "MODIFIED", "STAGED", "COMMITTED-IN-HEAD", "UNCHANGED")
    if state == "UNCHANGED":  # committed in an older commit: fake a MODIFIED header so cases 2/4 exercise the live path
        out = [f"edit_proof {me}: MODIFIED sha256={sha12(ROOT / me)}", "  +1 -0  (vs HEAD)", "  head=abc0000", f"✅ edit_proof: {me} MODIFIED"]
    foot = "\nATTEST tool=edit_proof sha256=0000000000000000 utc=2026-01-01T00:00:00Z head=abc0000 exit=0 cmd=x\n```\n"
    block = "```text\n" + "\n".join(out) + foot
    # 1) claim without proof → problem
    p, c, n = check_text(f"عدّلت {me} to add the check.\n")
    ok &= c == 1 and n == 0 and len(p) == 1
    # 2) claim with live proof → ok
    p, c, n = check_text(block + f"\nI fixed {me} so check() prints a table.\n")
    ok &= c == 1 and n == 1 and not p
    # 3) UNCHANGED proof → problem
    unch = f"```text\nedit_proof {me}: UNCHANGED sha256={sha12(ROOT / me)}\n  head=abc0000\n⛔ edit_proof: {me} UNCHANGED — nothing was edited" + foot
    p, c, n = check_text(unch + f"\nedited {me}.\n")
    ok &= c == 1 and len(p) == 1 and "UNCHANGED" in p[0]
    # 4) stale sha → problem
    stale = block.replace(out[0], f"edit_proof {me}: MODIFIED sha256=deadbeef0000")
    p, c, n = check_text(stale + f"\nedited {me}.\n")
    ok &= len(p) == 1 and "stale" in p[0]
    # 5) edit verb inside tool block only → no claim
    p, c, n = check_text("```text\nedited foo.py\nATTEST tool=attest sha256=0000000000000000 utc=2026-01-01T00:00:00Z head=abc0000 exit=0 cmd=x\n```\n")
    ok &= c == 0 and not p
    # 6) scope arithmetic (R92): hunk (10,3,·,·) touches HEAD 10-12; insertion (12,0) sits after line 12
    ok &= in_scope((10, 3, 10, 3), 10, 12) and not in_scope((10, 3, 10, 3), 11, 20) and not in_scope((9, 1, 9, 1), 10, 12)
    ok &= in_scope((12, 0, 13, 4), 10, 12) and in_scope((9, 0, 10, 4), 10, 12) and not in_scope((13, 0, 14, 1), 10, 12)
    # 7) real diff on an untracked scratch file → "cannot apply" + not ok ; scope parser rejects B<A
    scratch = ROOT / ".governance" / ".edit_proof_selftest.tmp"
    scratch.write_text("x\n", encoding="utf-8")
    try:
        lines, sok = scope_lines(".governance/.edit_proof_selftest.tmp", 1, 5)
        ok &= not sok and "cannot apply" in lines[0]
    finally:
        scratch.unlink()
    try:
        parse_scope(["show", "a.py", "--scope", "9-3"]); ok = False
    except SystemExit as e:
        ok &= e.code == 2
    ok &= parse_scope(["show", "a.py", "--scope", "3-9"]) == (["show", "a.py"], (3, 9))
    print("✅ edit_proof self-test ok (show / no-proof fails / live proof passes / UNCHANGED fails / stale fails / block-only ignored / scope ×3)" if ok
          else "⛔ edit_proof self-test FAILED")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    argv, scope = parse_scope(list(argv))
    if len(argv) >= 2 and argv[0] == "show":
        return show(argv[1:], scope)
    if len(argv) >= 2 and argv[0] == "check":
        return check(argv[1])
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
