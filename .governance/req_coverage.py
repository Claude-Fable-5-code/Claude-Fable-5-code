#!/usr/bin/env python3
"""
req_coverage.py — mechanical check for FULL_READ_PROTOCOL.md.

Reads an agent turn (file or stdin) containing a ```req-ledger``` block and a
```req-closure``` block, and verifies:
  1. every REQ-nn in the ledger has exactly one closure row
  2. no closure row refers to a REQ absent from the ledger
  3. every [Q] REQ is ANSWERED or BLOCKED (never DONE / DEFERRED / CTX)
  4. every [LINK] REQ is DONE or BLOCKED
  5. closure states are from the allowed set
  6. UNMAPPED is 'none'
  7. COVERAGE line present; warns if REQ count < 60% of SENTENCES
  8. --source FILE   : every ledger quote must occur VERBATIM (whitespace-normalised)
                       in the human's original message. Catches paraphrase drift (R37:
                       agent wrote يشوعها, human wrote يشوفها).
 10. --coverage-min P : (needs --source) at least P% of the source's non-space characters must
                       lie inside some ledger quote; prints every uncovered span >= 12 chars
                       (R47: "every character" — quotes-in-source proves nothing was invented,
                       coverage proves nothing was SKIPPED)
  9. --strict-done   : every DONE row must carry second-system proof: an https:// URL,
                       a CI run-id (8+ digits), or an 'origin/<ref>'. A bare commit hash
                       is NOT proof (it can exist only locally — R36: a84cbe0 was cited as
                       "pushed" while the push had failed). Use BLOCKED instead.

Exit 0 = pass. Exit 1 = violations. Exit 2 = blocks missing / malformed.
No dependencies, no network, no paths.

Usage:
  python .governance/req_coverage.py turn.md [--source human_msg.txt] [--strict-done]
  some_command | python .governance/req_coverage.py -
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ALLOWED = {"DONE", "ANSWERED", "RULE-KEPT", "CTX", "BLOCKED", "DEFERRED"}
LEDGER_RX = re.compile(r"```req-ledger\s*\n(.*?)```", re.S)
CLOSURE_RX = re.compile(r"```req-closure\s*\n(.*?)```", re.S)
LEDGER_ROW = re.compile(r"^\s*(REQ-\d{2,})\s+\[(ASK|Q|RULE|CTX|LINK)\]\s+\"(.+?)\"", re.M)
ANY_ROW = re.compile(r"^\s*(REQ-\d{2,})\s+\[([A-Z-]+)\]", re.M)
CLOSURE_ROW = re.compile(r"^\s*(REQ-\d{2,})\s+([A-Z-]+)\b(.*)$", re.M)
SENT_RX = re.compile(r"^\s*SENTENCES:\s*(\d+)", re.M)
COV_RX = re.compile(r"^\s*COVERAGE:", re.M)
UNMAPPED_RX = re.compile(r"^\s*UNMAPPED:\s*(.+)$", re.M)
PROOF_RX = re.compile(r"(https?://\S+|\b\d{8,}\b|\borigin/[\w./-]+)")  # a bare local hash is NOT proof (R36)
WS_RX = re.compile(r"\s+")


def norm(t: str) -> str:
    """Whitespace-normalise; strip quotes/ellipsis the agent may add around a quote."""
    return WS_RX.sub(" ", t.replace("…", " ").replace("\u201c", '"').replace("\u201d", '"')).strip()


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    strict_done = "--strict-done" in argv
    source_text: str | None = None
    if "--source" in argv:
        i = argv.index("--source")
        if i + 1 >= len(argv):
            print("⛔ req_coverage: --source needs a file"); return 2
        source_raw = Path(argv[i + 1]).read_text(encoding="utf-8", errors="replace")
        source_text = norm(source_raw)
        args = [a for a in args if a != argv[i + 1]]
    cov_min: float | None = None
    if "--coverage-min" in argv:
        j = argv.index("--coverage-min")
        if j + 1 >= len(argv) or source_text is None:
            print("⛔ req_coverage: --coverage-min needs a percentage and --source"); return 2
        cov_min = float(argv[j + 1]); args = [a for a in args if a != argv[j + 1]]
    if not args:
        print(__doc__); return 2
    src = sys.stdin.read() if args[0] == "-" else Path(args[0]).read_text(encoding="utf-8", errors="replace")

    lm, cm = LEDGER_RX.search(src), CLOSURE_RX.search(src)
    if not lm:
        print("⛔ req_coverage: no ```req-ledger``` block found (Step 1 skipped)"); return 2
    if not cm:
        print("⛔ req_coverage: no ```req-closure``` block found (Step 3 skipped)"); return 2

    problems: list[str] = []
    ledger = {m.group(1): (m.group(2), m.group(3)) for m in LEDGER_ROW.finditer(lm.group(1))}
    # R49: a row that LOOKS like a REQ but uses an unknown tag ([FIX] [VERIFY] [REPORT] …) was silently
    # skipped — so it inflated the REQ count in prose while escaping every check. Now it is a violation.
    for m in ANY_ROW.finditer(lm.group(1)):
        if m.group(1) not in ledger:
            problems.append(f"{m.group(1)} uses tag [{m.group(2)}] — only ASK|Q|RULE|CTX|LINK are valid (R49: unparsed rows are not REQs)")
    # R49b: SENTENCES/COVERAGE header must match parsed rows (no prose-only "23 REQs")
    sm = SENT_RX.search(lm.group(1))
    if sm and int(sm.group(1)) != len(ledger):
        problems.append(f"SENTENCES: says {sm.group(1)} but {len(ledger)} valid REQ rows parsed (R49)")
    closure_rows = CLOSURE_ROW.findall(cm.group(1))
    closure: dict[str, list[str]] = {}
    proof_text: dict[str, str] = {}
    for rid, state, rest in closure_rows:
        closure.setdefault(rid, []).append(state)
        proof_text[rid] = rest

    warnings: list[str] = []

    if not ledger:
        problems.append("ledger has zero parseable REQ rows (format: REQ-01 [ASK] \"quote\" → …)")

    for rid, (kind, quote) in ledger.items():
        # R48: verbatim check FIRST — must run even when the closure row is missing
        # (previously sat after `continue`, so unclosed REQs escaped the source check).
        if source_text is not None and norm(quote) not in source_text:
            problems.append(f"{rid} quote is NOT verbatim in --source (paraphrase drift, R37): \"{quote[:60]}\"")
        states = closure.get(rid)
        if not states:
            problems.append(f"{rid} [{kind}] has NO closure row — dropped: \"{quote[:50]}\"")
            continue
        if len(states) > 1:
            problems.append(f"{rid} has {len(states)} closure rows (must be exactly 1)")
        st = states[0]
        if st not in ALLOWED:
            problems.append(f"{rid} closure state '{st}' not in {sorted(ALLOWED)}")
        if kind == "Q" and st not in {"ANSWERED", "BLOCKED"}:
            problems.append(f"{rid} is a QUESTION but closed as {st} — questions must be ANSWERED or BLOCKED")
        if kind == "LINK" and st not in {"DONE", "BLOCKED"}:
            problems.append(f"{rid} is a LINK but closed as {st} — links must be read (DONE) or BLOCKED")
        if kind == "RULE" and st not in {"RULE-KEPT", "BLOCKED"}:
            problems.append(f"{rid} is a RULE but closed as {st} — rules must be RULE-KEPT or BLOCKED")
        if strict_done and st == "DONE" and not PROOF_RX.search(proof_text.get(rid, "")):
            problems.append(f"{rid} DONE without second-system proof (URL / run-id / origin/<ref>; a local hash does not count) — use BLOCKED if push/CI is pending (Rule 4)")

    for rid in closure:
        if rid not in ledger:
            problems.append(f"{rid} appears in closure but not in ledger (invented after the fact)")

    um = UNMAPPED_RX.search(cm.group(1))
    if not um:
        problems.append("closure lacks 'UNMAPPED:' line")
    elif um.group(1).strip().lower() != "none":
        problems.append(f"UNMAPPED is not 'none': {um.group(1).strip()}")

    if not COV_RX.search(lm.group(1)):
        problems.append("ledger lacks 'COVERAGE:' line")
    sm = SENT_RX.search(lm.group(1))
    if sm:
        n_sent, n_req = int(sm.group(1)), len(ledger)
        if n_sent and n_req < 0.6 * n_sent:
            warnings.append(f"only {n_req} REQs for {n_sent} sentences (<60%) — ledger is probably short")
    else:
        problems.append("ledger lacks 'SENTENCES:' line")

    if cov_min is not None and source_text is not None:
        covered = bytearray(len(source_text))
        for _, (_, quote) in ledger.items():
            q = norm(quote)
            if not q: continue
            start = 0
            while (k := source_text.find(q, start)) != -1:
                covered[k:k + len(q)] = b"\x01" * len(q); start = k + 1
        sig = [i for i, ch in enumerate(source_text) if not ch.isspace()]
        hit = sum(1 for i in sig if covered[i])
        pct = 100.0 * hit / max(1, len(sig))
        # uncovered spans
        spans, cur = [], None
        for i, ch in enumerate(source_text):
            if not covered[i] and not ch.isspace():
                cur = [i, i] if cur is None else [cur[0], i]
            elif ch.isspace() and cur is not None and i - cur[1] <= 1:
                cur[1] = i
            else:
                if cur and cur[1] - cur[0] + 1 >= 12: spans.append(source_text[cur[0]:cur[1] + 1].strip())
                cur = None
        if cur and cur[1] - cur[0] + 1 >= 12: spans.append(source_text[cur[0]:cur[1] + 1].strip())
        line = f"source coverage {pct:.0f}% of non-space chars inside ledger quotes (min {cov_min:.0f}%)"
        if pct + 1e-9 < cov_min:
            problems.append(line + f" — {len(spans)} uncovered span(s):")
            problems.extend(f"    ⟪{sp[:90]}⟫" for sp in spans[:25])
        else:
            print(f"ℹ️  req_coverage: {line}")

    for w in warnings:
        print(f"⚠️  req_coverage: {w}")
    if problems:
        print(f"⛔ req_coverage: {len(problems)} violation(s)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"✅ req_coverage: {len(ledger)} REQs, all closed" + (f" ({len(warnings)} warning)" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
