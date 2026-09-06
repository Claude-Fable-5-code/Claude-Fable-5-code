#!/usr/bin/env python3
"""
intent_gate.py — ASK-BEFORE-ACT, made mechanical (R58, Round 9).

The owner's standing complaint: "when I say 'شوف هتعمل ايه وقبل ما تنفذ قولي' or
'شوف كده نرفع ايه ع جيت هاب؟؟' I want to know whether it UNDERSTOOD me — instead it runs
off and searches / edits / pushes." Prose rules did not fix this in 8 rounds, so:

  detect  — reads the saved human message, finds plan-only triggers, prints MODE.
  verify  — reads the agent's turn (markdown/log) and fails if MODE was PLAN-ONLY but the
            turn contains any action marker, or lacks the mandatory ```plan-only block.

Usage:
    python .governance/intent_gate.py detect  fixtures/human_msg_<n>.txt
    python .governance/intent_gate.py verify  <agent_turn.md> --human fixtures/human_msg_<n>.txt
    python .governance/intent_gate.py --self-test

PLAN-ONLY turn contract (Rule 19):
    ```plan-only
    UNDERSTOOD: <one line per thing the human asked, in the human's words, quoted>
    I WILL:     <numbered steps, each naming the exact command/file; nothing executed yet>
    I WILL NOT: <what is explicitly out of scope this turn>
    WAITING FOR: your "go" / correction
    ```
    …and nothing else that changes state. No "Ran command", no "Created", no "Edited",
    no git push, no PR, no file writes except saving the human message fixture itself.
"""
import re, sys

# Egyptian/MSA + English triggers. Loose spelling on purpose (ه/ة, ي/ى, missing hamza).
TRIGGERS = [
    r"قبل\s*ما\s*تنفذ", r"قبل\s*ما\s*تعمل", r"قبل\s*ما\s*تبدأ", r"قبل\s*ما\s*تبدا",
    r"قول+ي\s*(الاول|اولا|قبل)", r"قولي\s*ه?ا?\s*تعمل", r"ها?\s*تعمل\s*اي[هة]?\b",
    r"هتعمل\s*اي[هة]?", r"شوف\s*(كده\s*)?(ها?تعمل|نعمل|نرفع|هنرفع)\s*اي[هة]?",
    r"نرفع\s*اي[هة]?\s*ع", r"فاهم(ني)?\s*(ولا|و\s*لا|\?|؟)", r"انت\s*فاهم", r"اعرف\s*هل\s*هو\s*فاهم",
    r"متنفذ\s*حاجه", r"ما\s*تنفذ", r"من\s*غير\s*تنفيذ", r"بدون\s*تنفيذ", r"مجرد\s*خطه", r"خطه\s*بس", r"الخطه\s*بس",
    r"\bplan\s*only\b", r"\bdon'?t\s+(run|execute|do)\b", r"\bbefore\s+you\s+(run|execute|do|start)\b",
    r"\bwhat\s+(will|would)\s+you\s+do\b", r"\bdo\s+you\s+understand\b", r"\btell\s+me\s+first\b",
]
# What a PLAN-ONLY turn must not contain (agent log / tool-transcript markers + git/PR verbs).
ACTION_MARKERS = [
    r"^\s*Ran command:", r"^\s*Created\s+\S", r"^\s*Edited\s+\S", r"^\s*Deleted\s+\S", r"^\s*Wrote\s+\S",
    r"\bgit\s+(push|commit|merge|rebase|reset)\b", r"\bgh\s+pr\s+(create|merge)\b", r"\bmerge_pr\.py\b",
    r"Used tool:\s*(write|edit|bash|run|shell|create|delete|apply)", r"\bpushed\b", r"\bmerged\b", r"\bcommitted\b",
    r"تم\s*(الرفع|الدمج|التنفيذ|الحذف|الانشاء|الإنشاء|التعديل|التحديث)", r"رفعت", r"دمجت", r"نفذت", r"عدلت", r"حدثت\s+(الملف|ملف|الملفات)",
]
ALLOWED_ACTION_EXCEPTIONS = [r"fixtures/human_msg_"]  # saving the human message itself is always allowed
# The human DESCRIBING the rule ("when I say X…", "مثلا", "زي لما بقوله") is not INVOKING it.
META_CONTEXT = [r"لما\s*ب?ا?قول[هك]?", r"مثلا", r"زي\s*(مثلا|لما)", r"\bwhen\s+i\s+say\b", r"\bfor\s+example\b", r"\be\.g\.", r"\blike\s+when\b"]

def norm(s):
    return re.sub(r"\s+", " ", s.replace("ى", "ي").replace("ة", "ه").replace("أ", "ا").replace("إ", "ا").replace("آ", "ا"))

def detect_text(human, return_meta=False):
    h = norm(human)
    hits, meta = [], []
    for t in TRIGGERS:
        for m in re.finditer(t, h, flags=re.I):
            ctx = h[max(0, m.start() - 80): m.start()]
            (meta if any(re.search(mc, ctx, flags=re.I) for mc in META_CONTEXT) else hits).append(m.group(0))
    return (hits, meta) if return_meta else hits

def verify_text(turn, human):
    hits = detect_text(human)
    problems = []
    if not hits:
        return "ACT", hits, problems
    if "```plan-only" not in turn:
        problems.append("missing ```plan-only block (Rule 19)")
    else:
        block = turn.split("```plan-only", 1)[1].split("```", 1)[0]
        for key in ("UNDERSTOOD:", "I WILL:", "I WILL NOT:", "WAITING FOR:"):
            if key not in block:
                problems.append(f"plan-only block missing '{key}'")
        # UNDERSTOOD must quote the human: at least one 12+ char span of the human text inside it
        hn, bn = norm(human), norm(block)
        quoted = any(hn[i:i + 12] in bn for i in range(0, max(1, len(hn) - 12), 6))
        if not quoted:
            problems.append("UNDERSTOOD: contains no verbatim span (>=12 chars) of the human message — paraphrase is not understanding")
    for i, line in enumerate(turn.splitlines(), 1):
        for a in ACTION_MARKERS:
            if re.search(a, line, flags=re.I | re.M) and not any(re.search(e, line) for e in ALLOWED_ACTION_EXCEPTIONS):
                problems.append(f"line {i}: action marker in PLAN-ONLY turn → {line.strip()[:90]}")
                break
    return "PLAN-ONLY", hits, problems

def self_test():
    h1 = "شوف كده نرفع ايه ع جيت هاب؟؟ وقبل ما تنفذ قولي"
    assert detect_text(h1), "trigger not detected"
    assert not detect_text("نفذ الخطة ورفع على جيت هاب حالا"), "false positive"
    bad = "Ran command: `git push origin main`\nتم الرفع بنجاح"
    mode, _, probs = verify_text(bad, h1)
    assert mode == "PLAN-ONLY" and probs, "bad turn passed"
    good = "```plan-only\nUNDERSTOOD: \"شوف كده نرفع ايه ع جيت هاب؟؟\" — you want the LIST, not the push\nI WILL: 1) list files… \nI WILL NOT: push, commit, edit\nWAITING FOR: your go\n```"
    mode, _, probs = verify_text(good, h1)
    assert mode == "PLAN-ONLY" and not probs, f"good turn failed: {probs}"
    # real Round-9 sentence: the human DESCRIBES the rule → META, not a trigger
    hits, meta = detect_text('لما بقوله مثلا شوف ها تعمل اي و قبل ما تنفذ قولي "او لما اقوله ها تعمل اي"', return_meta=True)
    assert meta and not hits, f"round9 meta phrase misclassified: hits={hits} meta={meta}"
    # same words WITHOUT meta framing → real trigger
    assert detect_text("شوف ها تعمل اي و قبل ما تنفذ قولي"), "bare round9 phrase missed"
    print("✅ intent_gate self-test ok (trigger / no-trigger / bad turn / good turn / meta vs bare round-9 phrase)")

def main(argv):
    if "--self-test" in argv:
        return self_test() or 0
    if len(argv) < 2:
        print(__doc__); return 2
    cmd, path = argv[0], argv[1]
    if cmd == "detect":
        hits, meta = detect_text(open(path, encoding="utf-8").read(), return_meta=True)
        if meta:
            print("META (human is describing the rule, not invoking it):", " | ".join(dict.fromkeys(meta)))
        if hits:
            print("MODE: PLAN-ONLY  — triggers:", " | ".join(dict.fromkeys(hits)))
            print("→ This turn: ```plan-only block, zero actions, then STOP and wait (Rule 19).")
            return 0
        print("MODE: ACT  — no ask-before-act trigger found"); return 0
    if cmd == "verify":
        human = open(argv[argv.index("--human") + 1], encoding="utf-8").read()
        turn = open(path, encoding="utf-8").read()
        mode, hits, probs = verify_text(turn, human)
        print(f"intent_gate verify: mode={mode} triggers={len(hits)} problems={len(probs)}")
        for p in probs:
            print("  ⛔", p)
        return 1 if probs else 0
    print(__doc__); return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
