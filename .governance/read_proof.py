#!/usr/bin/env python3
"""
read_proof.py — a diagnosis is allowed only after the WHOLE file was read, and the reading is on the record
(R84, Round 12, Rule 28).

Usage:
    python .governance/read_proof.py index <file> [<file>…]     # print a read-proof block per file (run via attest.py)
    python .governance/read_proof.py check <turn.md>            # exit 1 if the turn diagnoses without a matching proof
    python .governance/read_proof.py --self-test

Why this exists (Round 12). The human, verbatim:
    "لو جينا نعمل سكربت بيكون ف زي هلوسه اني بقولك عاوز مثلا اعدل او اشوف فين خطاء او ليه مش شغال
     بيكون منك تخمين و مش بتشوف سكربت كامل للنهايه"
The agent greps for a symbol, reads 40 lines around it, and names "the bug". Nothing in the transcript
distinguishes that from having read the file. This tool makes the distinction mechanical:

  index  → for every file, emit
              read_proof <path>: <N> lines sha256=<12 hex>
                L<a>-L<b>  <kind> <name>          (every def / class / async def / top-level section)
                …
              ✅ read_proof: <path> indexed end-to-end (<N> lines)
           The line count is `wc -l`+1 semantics (number of lines), the sha is over the bytes. The INDEX is
           computed from the whole file, so it cannot be produced from a partial read. Run under attest.py so
           the block carries an ATTEST footer (Rule 21).

  check  → scan the PROSE of a turn for DIAGNOSIS verbs ("the bug is", "root cause", "السبب", "الخطأ في",
           "الغلط في", "المشكلة في", "fix is", "الحل") that mention a file path or symbol. For each such sentence
           there must be a read_proof block in the same turn for a file whose recorded LINES and SHA256 match
           the file on disk right now (so the proof is of THIS version, not last week's). Otherwise exit 1.

Only prose is scanned; tool blocks are excluded (same splitter as claim_check).
"""
import hashlib, pathlib, re, sys

GOV = pathlib.Path(__file__).resolve().parent
ROOT = GOV.parent
sys.path.insert(0, str(GOV))
from attest import blocks  # noqa: E402
from claim_check import prose_and_blocks  # noqa: E402

DIAG = re.compile(
    r"(the\s+(bug|error|problem|issue|root\s+cause|cause|fix)\s+(is|was|lies|comes)|root\s+cause|"
    r"السبب|الخط[أا]\s*(في|هو|كان)|الغلط\s*(في|هو)|المشكل[ةه]\s*(في|هي|كانت|ان|أن)|الحل\s*(هو|ان|أن|في)|"
    r"مش\s*شغال\s*(بسبب|لان|لأن)|بسبب\s+(ان|أن)|because\s+the\s+\w+\s+(is|was|does|never|returns))",
    re.I)
PATHISH = re.compile(r"[\w./-]+\.(py|js|ts|tsx|jsx|sh|yml|yaml|json|md|toml|ini|cfg|ps1)\b|\b[a-zA-Z_][a-zA-Z0-9_]*\(\)", re.I)
HDR = re.compile(r"^read_proof (\S+): (\d+) lines sha256=([0-9a-f]{12})$")
SYM = re.compile(r"^(\s*)(async\s+def|def|class)\s+([A-Za-z_][A-Za-z0-9_]*)|^(#{1,3})\s+(.+?)\s*$|^\[([^\]]+)\]\s*$|^(?:export\s+)?(?:async\s+)?(function|class|const|let)\s+([A-Za-z_$][\w$]*)")
PROSE_EXT = {".md", ".txt", ".rst"}   # '#' is a heading only here; elsewhere it is a comment
INI_EXT = {".ini", ".cfg", ".toml"}   # '[section]' only here


def sha12(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def index_file(path: str):
    p = pathlib.Path(path)
    data = p.read_bytes()
    text = data.decode("utf-8", errors="replace")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    n = len(lines)
    ext = p.suffix.lower()
    marks = []
    for i, ln in enumerate(lines, 1):
        m = SYM.match(ln)
        if not m:
            continue
        if m.group(2):
            marks.append((i, len(m.group(1)), m.group(2).split()[-1], m.group(3)))
        elif m.group(4) and ext in PROSE_EXT:
            marks.append((i, len(m.group(4)) - 1, "section", m.group(5)[:60]))
        elif m.group(6) and ext in INI_EXT:
            marks.append((i, 0, "ini-section", m.group(6)[:60]))
        elif m.group(7) and ext not in PROSE_EXT:
            marks.append((i, 0, m.group(7), m.group(8)))
    out = [f"read_proof {path}: {n} lines sha256={sha12(data)}"]
    for k, (start, indent, kind, name) in enumerate(marks):
        # a symbol's span ends where the next symbol at the same-or-lower indent starts
        end = n
        for s2, ind2, _, _ in marks[k + 1:]:
            if ind2 <= indent:
                end = s2 - 1
                break
        out.append(f"  L{start}-L{end}  {kind} {name}")
    if not marks:
        out.append(f"  L1-L{n}  (no symbols — plain text/data; read as one span)")
    out.append(f"✅ read_proof: {path} indexed end-to-end ({n} lines)")
    return out, n, sha12(data)


def proofs_in(turn_text: str):
    """(path, lines, sha) for every read_proof block in the turn (fenced or footer-delimited)."""
    found = []
    for tool, body in blocks(turn_text):
        if tool != "read_proof":
            continue
        m = HDR.match(body[0].strip())
        if m:
            found.append((m.group(1), int(m.group(2)), m.group(3)))
    return found


def check_turn(turn_text: str, root: pathlib.Path = ROOT):
    prose, _ = prose_and_blocks(turn_text)
    proofs = proofs_in(turn_text)
    problems = []
    live = {}
    for path, n, sha in proofs:
        fp = (root / path) if not pathlib.Path(path).is_absolute() else pathlib.Path(path)
        if not fp.exists():
            live[path] = ("MISSING", None, None)
            continue
        _, n2, sha2 = index_file(str(fp))
        live[path] = ("OK" if (n == n2 and sha == sha2) else "STALE", n2, sha2)
    diag_sentences = []
    for sent in re.split(r"(?<=[.!?؟\n])\s+", prose):
        if DIAG.search(sent) and PATHISH.search(sent):
            diag_sentences.append(" ".join(sent.split())[:140])
    if diag_sentences and not proofs:
        for s in diag_sentences:
            problems.append(f"diagnosis with no read_proof block in this turn (Rule 28) → …{s}…")
    for path, (st, n2, sha2) in live.items():
        if st == "STALE":
            problems.append(f"read_proof for {path} is of a DIFFERENT version than the file now on disk ({n2} lines sha={sha2}) — re-index before diagnosing")
        elif st == "MISSING":
            problems.append(f"read_proof names {path} but it does not exist in this checkout")
    if diag_sentences and proofs:
        # every diagnosis must mention at least one indexed path (by basename) — otherwise the proof is decorative
        names = {pathlib.Path(p).name.lower() for p, _, _ in proofs}
        for s in diag_sentences:
            hits = {m.group(0).split("/")[-1].lower() for m in PATHISH.finditer(s) if "." in m.group(0)}
            if hits and not (hits & names):
                problems.append(f"diagnosis names {sorted(hits)} but the turn's read_proof covers {sorted(names)} (Rule 28) → …{s}…")
    return problems, len(diag_sentences), len(proofs)


def self_test():
    ok = True
    me = str(GOV / "read_proof.py")
    out, n, sha = index_file(me)
    ok &= out[0].startswith("read_proof ") and any("def check_turn" in l for l in out) and out[-1].startswith("✅ read_proof")
    block = "```text\n" + "\n".join(out) + f"\nATTEST tool=read_proof sha256=0000000000000000 utc=2026-01-01T00:00:00Z head=abc0000 exit=0 cmd=x\n```\n"
    rel = ".governance/read_proof.py"
    block_rel = block.replace(me, rel)
    # 1) diagnosis without any proof → fail
    p, d, pr = check_turn("The bug is in .governance/read_proof.py: check_turn() never returns.\n")
    ok &= bool(p) and d == 1 and pr == 0
    # 2) same diagnosis with a live proof of that file → pass
    p, d, pr = check_turn(block_rel + "\nThe bug is in .governance/read_proof.py: check_turn() never returns.\n")
    ok &= not p and pr == 1
    # 3) proof of a different version (sha tampered) → fail as STALE
    stale = block_rel.replace(f"sha256={sha}", "sha256=deadbeef0000")
    p, _, _ = check_turn(stale + "\nالسبب في .governance/read_proof.py ان الدالة check_turn() غلط\n")
    ok &= any("DIFFERENT version" in x for x in p)
    # 4) proof of file A, diagnosis about file B → fail (decorative proof)
    p, _, _ = check_turn(block_rel + "\nالمشكلة في .governance/attest.py هي ان blocks() مش بتقرا الفوتر\n")
    ok &= any("decorative" in x or "covers" in x for x in p)
    # 5) no diagnosis at all → pass with nothing to check
    p, d, _ = check_turn("Listed the fixtures directory. Waiting for تمام.\n")
    ok &= not p and d == 0
    print("✅ read_proof self-test ok (index end-to-end / no-proof fails / live proof passes / stale fails / wrong-file fails)" if ok else "⛔ read_proof self-test FAILED")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if len(argv) < 2:
        print(__doc__); return 2
    cmd, paths = argv[0], argv[1:]
    if cmd == "index":
        rc = 0
        for path in paths:
            try:
                out, _, _ = index_file(path)
                print("\n".join(out))
            except OSError as e:
                print(f"⛔ read_proof: cannot read {path}: {e}"); rc = 1
        return rc
    if cmd == "check":
        text = sys.stdin.read() if paths[0] == "-" else pathlib.Path(paths[0]).read_text(encoding="utf-8", errors="replace")
        problems, d, pr = check_turn(text)
        for x in problems:
            print("🔴", x)
        if problems:
            print(f"⛔ read_proof: {len(problems)} diagnosis/proof problem(s) — {d} diagnosis sentence(s), {pr} proof block(s) (Rule 28)")
            return 1
        print(f"✅ read_proof: {d} diagnosis sentence(s) all backed by {pr} live read_proof block(s)" if d else "ℹ️  read_proof: no diagnosis in this turn — nothing to prove")
        return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
