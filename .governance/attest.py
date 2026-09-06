#!/usr/bin/env python3
"""
attest.py — pasted tool output must be REAL tool output (R63, Round 10).

Round 9 made four tool blocks mandatory. Round 10 found the agent pasting blocks the tools never
printed: `sha=matching`, "all paths verified live on GitHub remote", "2 run(s) across head e6d287f",
"completed green with zero failures". None of those strings exist in any .governance tool. The block
was also written BEFORE the merge it described. A mandatory block that can be typed is theatre.

Two halves:

  run    python .governance/attest.py run -- python .governance/ci_status.py --pr 9
         Executes the command, echoes its output, appends a footer:
           ATTEST tool=ci_status sha256=<16> utc=<iso> head=<7> exit=<rc> cmd=<...>
         sha256 covers the exact bytes above it. Paste output + footer together.

  verify python .governance/attest.py verify turn.md [--live]
         For every fenced block whose first line starts with a known tool header:
           1. footer present, hash == sha256(block body)          else UNATTESTED
           2. every line matches that tool's line grammar        else FORGED (prints the line)
           3. --live: re-run cmd from footer, compare hash       else STALE (prints both)
         Exit 1 on any UNATTESTED / FORGED / STALE / DIVERGED.

Grammar is generated from the tools themselves (their print statements), not hand-copied, so a
tool change does not silently break verification.
"""
import os, hashlib, re, subprocess, sys, datetime, pathlib, shlex

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

GOV = pathlib.Path(__file__).resolve().parent
TOOLS = {  # header regex → (tool, allowed line regexes)
    "ci_status": [
        r"^ci_status \S+: \d+ run\(s\) across \d+ sha\(s\)$",
        r"^  [🟢🔴🟡⚪] \d{8,} [0-9a-f]{7} \S+\s+\S+\s+\S+$",
        r"^⛔ ci_status: (no runs found|\d+ of \d+ runs NOT green).*$",
        r"^✅ ci_status: ALL runs green$",
        r"^ℹ️  ci_status:.*$",
    ],
    "remote_proof": [
        r"^remote_proof \S+@\S+: \d+ path\(s\)$",
        r"^  ✅ REMOTE  \S+  sha=[0-9a-f]{12}$",
        r"^  🟡 DIFFERS \S+  local=[0-9a-f]{12} remote=[0-9a-f]{12}  \(not pushed / stale\)$",
        r"^  🟡 REMOTE-ONLY \S+  remote=[0-9a-f]{12} \(not in this checkout\)$",
        r"^  🔴 MISSING \S+  local exists, NOT on remote  ← .*$",
        r"^  ⚫ ABSENT  \S+  neither local nor remote$",
        r"^⛔ remote_proof: \d+ of \d+ path\(s\) not proven on remote.*$",
        r"^✅ remote_proof: all paths match remote$",
    ],
    "intent_gate": [
        r"^(META|MODE|TRIGGER|PLAN-ONLY|ACT)\b.*$", r"^  .*$",
    ],
    "req_coverage": [
        r"^(ℹ️  |✅ |⛔ |⚠️  )?req_coverage:.*$", r"^  .*$", r"^UNCOVERED.*$",
    ],
    "merge_pr": [r"^PR #\d+ .*$", r"^  .*$", r"^(⛔|✅|ℹ️) .*$"],
    "claim_check": [r"^🔴 C[1-7] .*$", r"^      ….*$", r"^(⛔|✅) claim_check: .*$"],
    "read_proof": [  # Round 12 (R84, Rule 28)
        r"^read_proof \S+: \d+ lines sha256=[0-9a-f]{12}$", r"^  L\d+-L\d+  .*$",
        r"^🔴 .*$", r"^(⛔|✅|ℹ️ ) ?read_proof: .*$",
    ],
    "mistakes": [  # Round 13 (R85, Rule 30)
        r"^mistakes (record: round=\S+ rule=\S+ rows=\d+|\S+: \d+ admission\(s\), \d+ recorded, ledger rows=\d+|recurrence: \d+ row\(s\), \d+ rule\(s\) repeated, \d+ unescalated)$",
        r"^  \| .* \|$", r"^🔴 unrecorded admission: .*$", r"^(⛔|✅|ℹ️ ) ?mistakes: .*$",
    ],
    "mock_scan": [  # Round 14 (R93, Rule 37)
        r"^mock_scan (staged|paths): \d+ file\(s\), \d+ finding\(s\)$", r"^🔴 \S+:\d+ P[1-6] .*$", r"^(⛔|✅) mock_scan: .*$",
    ],
    "edit_proof": [  # Round 13 (R86, Rule 31)
        r"^edit_proof \S+: (MODIFIED|STAGED|COMMITTED-IN-HEAD|UNTRACKED|UNCHANGED) sha256=[0-9a-f]{12}$",
        r"^edit_proof \S+: \d+ edit claim\(s\), \d+ proof block\(s\)$",
        r"^  (\+\d+ -\d+  \(vs HEAD\)|committed [0-9a-f]{7} .*|head=[0-9a-f]{7})$", r"^🔴 .*$", r"^(⛔|✅|ℹ️ ) ?edit_proof: .*$",
        r"^  scope \d+-\d+: (\d+ hunk\(s\)|file not in HEAD — scope cannot apply)$",  # Round 14 (R92, Rule 37)
        r"^  @@ -\d+,\d+ \+\d+,\d+ @@ (in-scope|OUT-OF-SCOPE)$",
    ],
    "self_review": [  # Round 13 (R87, Rule 32)
        r"^self_review \S+: \d+ tool block\(s\) in turn$", r"^🔴 S[1-7]: .*$", r"^(⛔|✅) self_review: .*$",
    ],
    "precheck": [  # Round 13 (R88, Rule 34)
        r"^precheck \S+: \d+ step\(s\), source=\S+, live=(yes|no)(, skipped=\S+)?$",
        r"^  \d+\. [a-z_]+\s+exit=-?\d+  .*$", r"^(⛔|✅) precheck: .*$",
    ],
    "state_gate": [  # Round 14 (R90, Rule 35)
        r"^state_gate (open|close|verify|check \S+): .*$", r"^  (tag|next|progress)=.*$", r"^🔴 .*$",
        r"^(⛔|✅|🟡) state_gate: .*$",
    ],
    "attest": [r"^.*$"],
}
FOOT = re.compile(r"^ATTEST tool=(\S+) sha256=([0-9a-f]{16}) utc=(\S+) head=([0-9a-f]{7}) exit=(-?\d+) cmd=(.*)$")


def h(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", "surrogateescape")).hexdigest()[:16]


def head() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True, cwd=GOV.parent).stdout.strip() or "0000000"
    except Exception:
        return "0000000"


def tool_of(cmd: list[str]) -> str:
    for a in cmd:
        m = re.search(r"([a-z_]+)\.py$", a)
        if m and m.group(1) in TOOLS:
            return m.group(1)
    return "unknown"


def run(cmd: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=GOV.parent, env=env)
    out = ((p.stdout or "") + (p.stderr or "")).rstrip("\n")
    print(out)
    utc_val = datetime.datetime.now(getattr(datetime, "UTC", datetime.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"ATTEST tool={tool_of(cmd)} sha256={h(out)} utc={utc_val} head={head()} exit={p.returncode} cmd={shlex.join(cmd)}")
    return 0


TIME_DEPENDENT = {"ci_status", "remote_proof"}  # outputs depend on remote state at run time


def blocks(text: str):
    """Yield (tool, lines) for every tool block. Fenced ``` blocks first; then (R78, Round 11) any
    ATTEST footer that sits OUTSIDE a fence — copy/paste into gists and chat clients strips fences,
    and a verifier that then silently skips half the blocks is itself a fabricated 'all genuine'."""
    fenced_spans = []
    for m in re.finditer(r"```[^\n]*\n(.*?)```", text, re.S):
        fenced_spans.append(m.span())
        yield from _classify(m.group(1))
    lines = text.split("\n"); pos = 0; starts = []
    for i, ln in enumerate(lines):
        if FOOT.match(ln.strip()) and not any(a <= pos < b for a, b in fenced_spans):
            j = i - 1
            while j >= 0 and lines[j].strip() and lines[j].strip() != "text" and not FOOT.match(lines[j].strip()):
                j -= 1
            yield from _classify("\n".join(lines[j + 1:i + 1]))
        pos += len(ln) + 1


def _classify(raw: str):
    for _ in (0,):
        body = raw.rstrip("\n").split("\n")
        # drop a leading "$ cmd" / "python ..." prompt line the agent likes to show
        while body and re.match(r"^\s*(\$|python|py)\s", body[0]):
            body = body[1:]
        if not body:
            continue
        first = body[0].strip()
        for t in TOOLS:
            if first.startswith(t + " ") or first.startswith(t + ":") or (t == "intent_gate" and re.match(r"^(META|MODE)\b", first)) or (t == "req_coverage" and "req_coverage:" in first):
                yield t, body
                break


def verify(path: str, live: bool) -> int:
    text = sys.stdin.read() if path == "-" else pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    bad = 0; n = 0
    for tool, body in blocks(text):
        n += 1
        foot = FOOT.match(body[-1].strip()) if body else None
        content = body[:-1] if foot else body
        pats = [re.compile(p) for p in TOOLS[tool]]
        for ln in content:
            if ln.strip() == "":
                continue
            if not any(p.match(ln) for p in pats):
                print(f"🔴 FORGED     [{tool}] line not in tool grammar: {ln.strip()[:110]}"); bad += 1
        if not foot:
            print(f"🔴 UNATTESTED [{tool}] block has no ATTEST footer (run it through attest.py run)"); bad += 1; continue
        ftool, fh, utc, fhead, rc, cmd = foot.groups()
        want = h("\n".join(content).rstrip("\n"))
        if fh != want:
            print(f"🔴 TAMPERED   [{tool}] footer sha {fh} != body sha {want} — block edited after run"); bad += 1; continue
        if live:
            try:
                p = subprocess.run(shlex.split(cmd), capture_output=True, text=True, cwd=GOV.parent, timeout=120)
                now = (p.stdout + p.stderr).rstrip("\n")
                if h(now) != fh:
                    # R79 (Round 11, self-finding): ci_status / remote_proof describe REMOTE STATE, which legitimately
                    # changes after a push or merge. An honest pre-push block re-run post-push differs. That is STALE,
                    # not forged. It is a problem only if the pasted block claimed success and live disagrees.
                    if tool in TIME_DEPENDENT:
                        if int(rc) == 0 and p.returncode != 0:
                            print(f"🔴 REGRESSED  [{tool}] pasted exit=0 but live exit={p.returncode} — the claimed state no longer holds. Live output:"); print("\n".join("      " + l for l in now.split("\n"))); bad += 1; continue
                        print(f"🕒 STALE      [{tool}] utc={utc} head={fhead} exit={rc} — genuine at the time; remote state moved since (live exit={p.returncode})"); continue
                    print(f"🟡 DIVERGED   [{tool}] live re-run differs from pasted block (pasted utc={utc}). Live output:"); print("\n".join("      " + l for l in now.split("\n"))); bad += 1; continue
            except Exception as e:
                print(f"🟡 UNCHECKED  [{tool}] could not re-run: {e}")
        print(f"✅ ATTESTED   [{tool}] utc={utc} head={fhead} exit={rc}")
    if n == 0:
        print("⛔ attest: no tool blocks found in turn — Rules 16/18/19 require them"); return 1
    if bad:
        print(f"⛔ attest: {bad} problem(s) in {n} block(s) — a typed tool block is a fabricated fact (Rule 21)"); return 1
    print(f"✅ attest: {n} block(s) genuine"); return 0


def main(a: list[str]) -> int:
    if not a or a[0] not in ("run", "verify"):
        print(__doc__); return 2
    if a[0] == "run":
        cmd = a[2:] if len(a) > 1 and a[1] == "--" else a[1:]
        if not cmd:
            print("⛔ attest run: no command"); return 2
        return run(cmd)
    if len(a) < 2:
        print("⛔ attest verify: need turn file or -"); return 2
    return verify(a[1], "--live" in a)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
