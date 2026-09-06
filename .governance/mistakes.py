#!/usr/bin/env python3
"""
mistakes.py — an admitted mistake is a ledger row, not a sentence (R85, Round 13, Rule 30).

Usage:
    python .governance/mistakes.py record --round 13 --rule 25 "what went wrong, one line"
    python .governance/mistakes.py check <turn.md>          # exit 1 if prose admits a mistake with no row for it
    python .governance/mistakes.py --self-test

Why this exists (Round 13, RECONSTRUCTED after reset). Across Rounds 6-12 the agent wrote "I was wrong",
"غلطت", "my mistake" in prose at least once per round, and the same class of mistake came back the next
round. An admission that lives only in chat is forgotten by the next session. This tool makes the admission
a row in `.governance/MISTAKES.md`:

    | utc | round | rule | what |

  record → appends the row (utc is stamped by the tool, never typed). Run under attest.py.
  check  → scans the PROSE of a turn (tool blocks excluded) for ADMISSION phrases. For each admission
           sentence there must be a row in MISTAKES.md whose `what` shares ≥ 3 words (≥ 4 chars each) with
           the sentence, OR the turn must contain a `mistakes` tool block with exit=0 from `record`.
           Otherwise exit 1 and print the unrecorded sentence.

Only prose is scanned; a quoted admission inside a tool block is not an admission.
"""
import datetime, pathlib, re, sys

GOV = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(GOV))
from claim_check import prose_and_blocks  # noqa: E402

LEDGER = GOV / "MISTAKES.md"
HEADER = "# MISTAKES — admissions ledger (Rule 30). Rows are appended by mistakes.py only.\n\n| utc | round | rule | what |\n|---|---|---|---|\n"
ADMIT = re.compile(
    r"(\bI\s+was\s+wrong\b|\bmy\s+mistake\b|\bI\s+(mis(read|understood|took)|forgot|skipped|fabricated|typed\s+the\s+verdict)\b|"
    r"غلطت|كنت\s+مخطئ|خط[أا]\s+مني|أنا\s+غلطان|انا\s+غلطان|نسيت|فهمت\s+غلط|ماقريتش|ما\s*قرأت)", re.I)
WORD = re.compile(r"[\w]{4,}", re.U)
ROW = re.compile(r"^\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(.*?)\s*\|$")


def rows():
    if not LEDGER.exists():
        return []
    out = []
    for ln in LEDGER.read_text(encoding="utf-8").splitlines():
        m = ROW.match(ln.strip())
        if m and m.group(1) not in ("utc", "---"):
            out.append(m.groups())
    return out


def record(round_no: str, rule: str, what: str) -> int:
    what = " ".join(what.split()).replace("|", "/")
    if not what:
        print("⛔ mistakes: empty 'what' — a row with no content is not an admission"); return 1
    if not LEDGER.exists():
        LEDGER.write_text(HEADER, encoding="utf-8")
    utc = datetime.datetime.now(getattr(datetime, "UTC", datetime.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(f"| {utc} | {round_no} | {rule} | {what} |\n")
    print(f"mistakes record: round={round_no} rule={rule} rows={len(rows())}")
    print(f"  | {utc} | {round_no} | {rule} | {what} |")
    print("✅ mistakes: row appended to .governance/MISTAKES.md")
    return 0


def sentences(prose: str):
    for s in re.split(r"(?<=[.!?؟])\s+|\n+", prose):
        s = s.strip()
        if s:
            yield s


def check_text(text: str, ledger_rows=None):
    """Return (problems, admissions, recorded)."""
    prose, bl = prose_and_blocks(text)
    ledger_rows = rows() if ledger_rows is None else ledger_rows
    recorded_in_turn = any(t == "mistakes" and rc == 0 and any(l.startswith("mistakes record:") for l in body) for t, rc, body in bl)
    problems, admissions, recorded = [], 0, 0
    for s in sentences(prose):
        if not ADMIT.search(s):
            continue
        admissions += 1
        words = set(w.lower() for w in WORD.findall(s))
        hit = any(len(words & set(w.lower() for w in WORD.findall(r[3]))) >= 3 for r in ledger_rows)
        if hit or recorded_in_turn:
            recorded += 1
        else:
            problems.append(f"unrecorded admission: «{s[:120]}»")
    return problems, admissions, recorded


def check(path: str) -> int:
    text = pathlib.Path(path).read_text(encoding="utf-8")
    problems, adm, rec = check_text(text)
    print(f"mistakes {path}: {adm} admission(s), {rec} recorded, ledger rows={len(rows())}")
    for p in problems:
        print(f"🔴 {p}")
    if adm == 0:
        print("ℹ️  mistakes: no admission in this turn — nothing to record"); return 0
    if problems:
        print(f"⛔ mistakes: {len(problems)} admission(s) without a MISTAKES.md row — an unlogged mistake repeats (Rule 30)"); return 1
    print("✅ mistakes: every admission has a ledger row"); return 0


def self_test() -> int:
    ok = True
    fake = [("2026-01-01T00:00:00Z", "12", "25", "claimed PROGRESS.md updated without remote_proof block")]
    # 1) admission, no matching row → problem
    p, a, r = check_text("I was wrong: I typed the claim_check verdict in prose.\n", fake)
    ok &= a == 1 and r == 0 and len(p) == 1
    # 2) admission matching a row (≥3 shared words) → ok
    p, a, r = check_text("غلطت — I claimed PROGRESS.md updated without a remote_proof block.\n", fake)
    ok &= a == 1 and r == 1 and not p
    # 3) admission + record block in same turn → ok
    turn = ("My mistake: skipped the export.\n```text\nmistakes record: round=13 rule=33 rows=1\n  | x | 13 | 33 | skipped export |\n"
            "✅ mistakes: row appended to .governance/MISTAKES.md\nATTEST tool=mistakes sha256=0000000000000000 utc=2026-01-01T00:00:00Z head=abc0000 exit=0 cmd=x\n```\n")
    p, a, r = check_text(turn, [])
    ok &= a == 1 and r == 1 and not p
    # 4) admission phrase only inside a tool block → not an admission
    p, a, r = check_text("```text\nI was wrong here\nATTEST tool=attest sha256=0000000000000000 utc=2026-01-01T00:00:00Z head=abc0000 exit=0 cmd=x\n```\n", [])
    ok &= a == 0 and not p
    # 5) no admission at all
    p, a, r = check_text("All checks passed; see blocks above.\n", [])
    ok &= a == 0 and not p
    print("✅ mistakes self-test ok (unrecorded fails / ledger match / same-turn record / block-only ignored / none)" if ok
          else "⛔ mistakes self-test FAILED")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if len(argv) >= 2 and argv[0] == "check":
        return check(argv[1])
    if argv and argv[0] == "record":
        rnd = rule = "?"; rest = []
        it = iter(argv[1:])
        for a in it:
            if a == "--round": rnd = next(it, "?")
            elif a == "--rule": rule = next(it, "?")
            else: rest.append(a)
        return record(rnd, rule, " ".join(rest))
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
