#!/usr/bin/env python3
"""
self_review.py — a self-review that cannot say ❌ is decoration (R87, Round 13, Rule 32).

Usage:
    python .governance/self_review.py check <turn.md> [--human <msg.txt>]
    python .governance/self_review.py --self-test

Why this exists (Round 13, RECONSTRUCTED after reset). Every "self-critique" block the agent wrote in
Rounds 9-12 answered ✅ to every question. The human's finding: a review whose output is constant carries
zero bits. This tool requires a ```self-review block with six fixed questions, each answered with a mark
AND evidence, and rejects the block when it is all-✅ without an explicit reason per ❌-eligible question.

  Q1 attested:   every tool block in this turn has an ATTEST footer          ✅/❌  evidence: sha256=<16> of one block
  Q2 prechecked: precheck.py ran on THIS text                                 ✅/❌  evidence: sha256=<16> of the precheck block
  Q3 skipped:    which check I skipped and why (or "none")
  Q4 pleasing:   the sentence most likely written to please, quoted verbatim (or "none")
  Q5 re-read:    I re-read the human message after drafting                  ✅/❌  missed: «verbatim quote» | none missed
  Q6 remote:     anything called updated/saved/pushed has remote_proof REMOTE ✅/❌  evidence: … | none — nothing claimed

Checks (each is a printed problem):
  S1 block present, all six Q-lines present, in order
  S2 Q1/Q2 ✅ require `sha256=<16 hex>` that matches a footer sha of a block IN THIS TURN
  S3 Q3 is "none" only if the turn contains ≥ 3 distinct tool families (you cannot have skipped nothing with one block)
  S4 Q4 quote (if not "none") must appear verbatim in the PROSE of this turn
  S5 Q5 ✅ requires the `missed:` field; if it quotes a sentence, that sentence must be verbatim in --human (when given)
  S6 Q6 ✅ requires a remote_proof block with "✅ remote_proof: all paths match remote"; ❌ requires "evidence: none"
  S7 at least one ❌ OR every ✅ carries evidence that S2/S5/S6 verified — all-✅ with no verifiable evidence fails
"""
import pathlib, re, sys

GOV = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(GOV))
from claim_check import prose_and_blocks  # noqa: E402
from attest import FOOT  # noqa: E402

QS = ["Q1 attested:", "Q2 prechecked:", "Q3 skipped:", "Q4 pleasing:", "Q5 re-read:", "Q6 remote:"]
SHA = re.compile(r"sha256=([0-9a-f]{16})")
NONE = re.compile(r"^\s*none\b", re.I)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')).strip()


def find_block(text: str):
    m = re.search(r"```self-review[^\n]*\n(.*?)```", text, re.S)
    return m.group(1) if m else None


def parse(block: str):
    q = {}
    for ln in block.splitlines():
        for k in QS:
            if ln.strip().startswith(k):
                q[k] = ln.strip()[len(k):].strip()
    return q


def _mark(v: str):
    return "✅" if v.startswith("✅") else "❌" if v.startswith("❌") else None


def check_text(text: str, human: str | None = None):
    prose, bl = prose_and_blocks(text)
    problems = []
    block = find_block(text)
    if block is None:
        return ["S1: no ```self-review block"], 0
    q = parse(block)
    missing = [k for k in QS if k not in q]
    if missing:
        problems.append(f"S1: missing {', '.join(missing)}")
    order = [k for k in QS if k in q]
    if order != [k for k in QS if k in order]:
        problems.append("S1: questions out of order")
    footer_shas = {FOOT.match(b[-1].strip()).group(2) for _, _, b in bl if b and FOOT.match(b[-1].strip())}
    families = {t for t, _, _ in bl}
    # S2
    for k in ("Q1 attested:", "Q2 prechecked:"):
        v = q.get(k, "")
        if _mark(v) == "✅":
            m = SHA.search(v)
            if not m:
                problems.append(f"S2: {k} ✅ without sha256=<16> evidence")
            elif m.group(1) not in footer_shas:
                problems.append(f"S2: {k} sha {m.group(1)} is not a footer of any block in this turn")
        elif _mark(v) is None and v:
            problems.append(f"S2: {k} has no ✅/❌ mark")
    # S3
    a3 = q.get("Q3 skipped:", "")
    if NONE.match(a3) and len(families) < 3:
        problems.append(f"S3: Q3 'none' with only {len(families)} tool famil(y/ies) in the turn — something was skipped")
    # S4
    a4 = q.get("Q4 pleasing:", "")
    if a4 and not NONE.match(a4):
        quoted = norm(a4).strip("«»\"' ")
        quoted = re.split(r"\s+[—-]\s+", quoted)[0].strip("«»\"' ")
        if quoted and quoted[:40] not in norm(prose):
            problems.append("S4: Q4 quote is not verbatim in this turn's prose")
    # S5
    a5 = q.get("Q5 re-read:") or ""
    if a5 and _mark(a5) == "✅":
        mm = re.search(r"missed:\s*(.*)$", a5, re.I | re.S)
        if not mm or not mm.group(1).strip():
            problems.append("S5: Q5 ✅ requires 'missed: <sentence | none missed>'")
        elif human and not NONE.match(mm.group(1)):
            quoted = norm(mm.group(1)).strip("«»\"' ")
            if quoted and quoted[:40] not in norm(human):
                problems.append("S5: Q5 'missed:' quote is not verbatim in the human message")
    # S6
    a6 = q.get("Q6 remote:", "")
    rp_ok = any(t == "remote_proof" and any("✅ remote_proof: all paths match remote" in l for l in b) for t, _, b in bl)
    if _mark(a6) == "✅" and not rp_ok:
        problems.append("S6: Q6 ✅ without a remote_proof block saying all paths match remote")
    if _mark(a6) == "❌" and "evidence: none" not in a6.lower() and "remote_proof" not in a6.lower():
        problems.append("S6: Q6 ❌ must say 'evidence: none' or cite the remote_proof block")
    # S7
    marks = [_mark(q.get(k, "")) for k in ("Q1 attested:", "Q2 prechecked:", "Q5 re-read:", "Q6 remote:")]
    if marks and all(m == "✅" for m in marks) and not any(p.startswith("S2") or p.startswith("S5") or p.startswith("S6") for p in problems):
        # all ✅ AND all verified — allowed only when the evidence was verifiable (S2 shas matched, S6 rp_ok)
        if not rp_ok:
            problems.append("S7: all-✅ review but no remote_proof REMOTE — at least one ❌ was due")
    return problems, len(bl)


def check(path: str, human_path: str | None) -> int:
    text = pathlib.Path(path).read_text(encoding="utf-8")
    human = pathlib.Path(human_path).read_text(encoding="utf-8") if human_path else None
    problems, n = check_text(text, human)
    print(f"self_review {path}: {n} tool block(s) in turn")
    for p in problems:
        print(f"🔴 {p}")
    if problems:
        print(f"⛔ self_review: {len(problems)} problem(s) — a review that cannot say ❌ is decoration (Rule 32)"); return 1
    print("✅ self_review: block present, every mark carries verifiable evidence"); return 0


def self_test() -> int:
    ok = True
    foot = "ATTEST tool={t} sha256={s} utc=2026-01-01T00:00:00Z head=abc0000 exit=0 cmd=x"
    b1 = "```text\nmistakes x: 0 admission(s), 0 recorded, ledger rows=2\nℹ️  mistakes: no admission in this turn — nothing to record\n" + foot.format(t="mistakes", s="a" * 16) + "\n```\n"
    b2 = "```text\nremote_proof o@m: 1 path(s)\n  🔴 MISSING x  local exists, NOT on remote  ← y\n⛔ remote_proof: 1 of 1 path(s) not proven on remote\n" + foot.format(t="remote_proof", s="b" * 16) + "\n```\n"
    b3 = "```text\nintent_gate verify: mode=ACT\n" + foot.format(t="intent_gate", s="c" * 16) + "\n```\n"
    prose = "I re-checked everything and it works.\n"
    good = ("```self-review\nQ1 attested:   ✅  evidence: sha256=" + "a" * 16 + "\nQ2 prechecked: ✅  evidence: sha256=" + "c" * 16 +
            "\nQ3 skipped:    attest --live — blocks are seconds old\nQ4 pleasing:   «I re-checked everything and it works.»\n"
            "Q5 re-read:    ✅  missed: «push-per-chunk»\nQ6 remote:     ❌  evidence: none — remote_proof says MISSING\n```\n")
    human = "أنفّذ بchunks صغيرة مدفوعة (push-per-chunk لمقاومة الـresets)"
    p, n = check_text(b1 + b2 + b3 + prose + good, human); ok &= not p and n == 3
    # no block
    p, _ = check_text(b1 + prose); ok &= any(x.startswith("S1") for x in p)
    # sha not in turn
    p, _ = check_text(b1 + b2 + b3 + prose + good.replace("a" * 16, "f" * 16)); ok &= any("S2" in x for x in p)
    # all-✅ with Q6 ✅ but remote_proof MISSING
    p, _ = check_text(b1 + b2 + b3 + prose + good.replace("Q6 remote:     ❌  evidence: none — remote_proof says MISSING", "Q6 remote:     ✅  evidence: pushed"))
    ok &= any("S6" in x for x in p)
    # Q4 quote not in prose
    p, _ = check_text(b1 + b2 + b3 + prose + good.replace("I re-checked everything and it works.", "Everything is perfect now.")); ok &= any("S4" in x for x in p)
    # Q5 missed quote not in human
    p, _ = check_text(b1 + b2 + b3 + prose + good.replace("«push-per-chunk»", "«something else»"), human); ok &= any("S5" in x for x in p)
    # Q3 none with 1 family
    p, _ = check_text(b1 + prose + good.replace("attest --live — blocks are seconds old", "none").replace("c" * 16, "a" * 16)); ok &= any("S3" in x for x in p)
    print("✅ self_review self-test ok (good passes / no block / foreign sha / Q6 ✅ w/o REMOTE / Q4 not verbatim / Q5 not in human / Q3 none)" if ok
          else "⛔ self_review self-test FAILED")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if len(argv) >= 2 and argv[0] == "check":
        human = argv[argv.index("--human") + 1] if "--human" in argv and argv.index("--human") + 1 < len(argv) else None
        return check(argv[1], human)
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
