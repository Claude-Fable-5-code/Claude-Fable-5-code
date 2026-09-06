#!/usr/bin/env python3
"""
precheck.py — the turn is checked BEFORE it is sent, by the tools, not by the author (R88, Round 13, Rule 34).

Usage:
    python .governance/precheck.py <turn.md> --source <human_msg.txt> [--live] [--skip name,name]
    python .governance/precheck.py --self-test

Why this exists (Round 13, RECONSTRUCTED after reset). Rounds 9-12 added seven checkers. Every one of them
was run by the HUMAN on the agent's turn after it was sent, and every round found violations the agent
could have found itself. This tool runs the whole family on the draft, in dependency order, and stops at
the first failure so the agent fixes and re-runs instead of sending:

    1 intent_gate verify   (mode; CONFIRM-FIRST mirror contract)
    2 attest verify        (every tool block genuine; --live re-runs commands)
    3 claim_check          (prose vs blocks, C1-C7)
    4 read_proof check     (diagnosis needs a full-file proof)
    5 edit_proof check     (edit claim needs a live diff)
    6 mistakes check       (admission needs a ledger row)
    7 self_review check    (six questions, evidence, ≥ 1 ❌ or verified ✅)
    8 req_coverage         (ledger/closure; --strict-done --coverage-min 85)   — only if a req-ledger block exists

Output is one line per step (`  n. tool  exit=k  <last line of tool output>`) then a verdict line.
Run it under attest.py so the table itself carries an ATTEST footer; paste that block in the turn, then
self_review Q2 cites its sha. Exit 1 at the first failing step. `--skip a,b` is allowed only with a
reason that goes in self_review Q3.
"""
import pathlib, re, subprocess, sys

GOV = pathlib.Path(__file__).resolve().parent
ROOT = GOV.parent
PY = sys.executable


def steps(turn: str, source: str | None, live: bool):
    hum = ["--human", source] if source else []
    src = ["--source", source] if source else []
    s = [
        ("intent_gate", [PY, str(GOV / "intent_gate.py"), "verify", turn, *hum]),
        ("attest", [PY, str(GOV / "attest.py"), "verify", turn, *(["--live"] if live else [])]),
        ("claim_check", [PY, str(GOV / "claim_check.py"), turn]),
        ("read_proof", [PY, str(GOV / "read_proof.py"), "check", turn]),
        ("edit_proof", [PY, str(GOV / "edit_proof.py"), "check", turn]),
        ("mistakes", [PY, str(GOV / "mistakes.py"), "check", turn]),
        ("self_review", [PY, str(GOV / "self_review.py"), "check", turn, *hum]),
    ]
    text = pathlib.Path(turn).read_text(encoding="utf-8", errors="replace")
    if "```req-ledger" in text:
        s.append(("req_coverage", [PY, str(GOV / "req_coverage.py"), turn, "--strict-done", *src, *(["--coverage-min", "85"] if source else [])]))
    return s


def run(turn: str, source: str | None, live: bool, skip: set[str]) -> int:
    plan = [(n, c) for n, c in steps(turn, source, live) if n not in skip]
    print(f"precheck {turn}: {len(plan)} step(s), source={source or '-'}, live={'yes' if live else 'no'}"
          + (f", skipped={','.join(sorted(skip))}" if skip else ""))
    for i, (name, cmd) in enumerate(plan, 1):
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT,
                           env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
        out = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()
        last = out[-1] if out else "(no output)"
        print(f"  {i}. {name:<13} exit={p.returncode}  {last[:140]}")
        if p.returncode != 0:
            print(f"⛔ precheck: stopped at step {i} ({name}) exit={p.returncode} — fix, re-run; do not send (Rule 34)")
            return 1
    print(f"✅ precheck: {len(plan)}/{len(plan)} steps exit 0 — turn may be sent")
    return 0


def self_test() -> int:
    import tempfile
    ok = True
    d = pathlib.Path(tempfile.mkdtemp())
    human = d / "h.txt"; human.write_text("نفّذ الخطة بchunks صغيرة.\n", encoding="utf-8")
    # 1) a turn with no blocks → attest (step 2) refuses: Rules 16/18/19 require blocks
    bad = d / "bad.md"; bad.write_text("Done. Everything is pushed and green.\n", encoding="utf-8")
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = run(str(bad), str(human), False, set())
    ok &= rc == 1 and "stopped at step 2 (attest)" in buf.getvalue()
    # 2) --skip removes a step from the plan
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = run(str(bad), str(human), False, {"claim_check", "attest"})
    ok &= "skipped=attest,claim_check" in buf.getvalue() and "1. intent_gate" in buf.getvalue() and "2. read_proof" in buf.getvalue()
    # 3) a turn with a fabricated (unattested) block → stops at attest (step 2)
    forged = d / "forged.md"; forged.write_text("```text\nremote_proof o@m: 1 path(s)\n✅ remote_proof: all paths match remote\n```\nAll pushed.\n", encoding="utf-8")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = run(str(forged), str(human), False, set())
    ok &= rc == 1 and "2. attest" in buf.getvalue() and "stopped at step 2" in buf.getvalue()
    print("✅ precheck self-test ok (no-block turn stops at attest / --skip honoured / forged block stops at attest)" if ok
          else "⛔ precheck self-test FAILED")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if not argv or argv[0].startswith("--"):
        print(__doc__); return 2
    turn = argv[0]
    source = argv[argv.index("--source") + 1] if "--source" in argv and argv.index("--source") + 1 < len(argv) else None
    skip = set(argv[argv.index("--skip") + 1].split(",")) if "--skip" in argv and argv.index("--skip") + 1 < len(argv) else set()
    return run(turn, source, "--live" in argv, skip)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
