# FULL READ PROTOCOL — every character, every line, every question

**Tier:** T0. Applies to every AI agent turn that responds to a human message on this project.
**Enforced by:** `python .governance/req_coverage.py` (mechanical) + the human counting rows (30 seconds).

---

## The honest premise

You cannot make a language model "read harder." It already sees every token. What goes wrong is downstream: it **acts on a compressed version** of what it saw — merging two requests into one, treating a question as a statement, answering the loud part and dropping the quiet part.

So this protocol does not ask the agent to read carefully. It asks the agent to **produce an artifact that is impossible to produce without having processed every sentence**, and it makes that artifact **countable** so the human can verify coverage in seconds without re-reading their own message.

---

## Step 1 — REQ ledger BEFORE any tool call

The agent's first output in the turn is a fenced block:

```req-ledger
SOURCE: <first 6 words of the human message> … <last 6 words>
SENTENCES: <N>            ← count of sentences/clauses in the human message
REQ-01 [ASK]   "<verbatim quote>"           → <one-line restatement>
REQ-02 [Q]     "<verbatim quote>"           → question — must receive an explicit answer
REQ-03 [RULE]  "<verbatim quote>"           → standing constraint for this and future turns
REQ-04 [CTX]   "<verbatim quote>"           → context only, no action needed
…
REQ-NN
COVERAGE: <NN> REQs from <N> sentences — <list of sentence numbers NOT mapped, or "none">
```

Rules for the ledger:
- **Verbatim quote** = the human's exact words (any language), not a paraphrase. Minimum: enough to `grep` it in the original.
- Every sentence maps to at least one REQ. Sentences that carry no request are tagged `[CTX]` — they still appear.
- A sentence with two imperatives ("do X and also Y") becomes two REQs.
- A question mark, or an interrogative in any language ("ازاي", "هل", "ليه", "why", "how"), **always** produces a `[Q]` REQ.
- A constraint stated once ("never leave anything uncommitted", "اوعي تنسي") becomes a `[RULE]` REQ and is copied into `Root/ANCHORS.md` if not already there.
- Links pasted by the human are each a REQ: `[LINK] "<url>" → read fully; report what it contains`.

## Step 2 — Work

Normal execution. Each tool call or file edit references the REQ ids it serves (`# REQ-03, REQ-07`). Commit messages include `Closes: REQ-xx, REQ-yy`.

## Step 3 — Closure table at the END of the turn

```req-closure
REQ-01 DONE      <proof: file / command output / commit hash>
REQ-02 ANSWERED  <the answer, one line, or pointer to the section>
REQ-03 RULE-KEPT <how it was honoured this turn>
REQ-04 CTX       —
REQ-05 BLOCKED   <what is needed from the human, exactly>
REQ-06 DEFERRED  <to which task id / next turn; why it could not be done now>
UNMAPPED: none
```

Allowed states: `DONE | ANSWERED | RULE-KEPT | CTX | BLOCKED | DEFERRED`. Nothing else. **Every REQ from Step 1 appears exactly once.** A REQ that appears in the ledger but not in the closure is a T1 violation — same weight as a failing CI gate.

## Step 4 — Mechanical check

```
python .governance/req_coverage.py <turn.md> --strict-done --source <human_message.txt>
```
Exit 0 only when: every `REQ-nn` in the ledger has a closure row; every `[Q]` is `ANSWERED` or `BLOCKED` (never `DEFERRED`, never `DONE`); `UNMAPPED` is `none`; no closure row exists without a ledger row; **(`--source`)** every ledger quote occurs verbatim in the human's message — save the message to a file first, the agent's memory of it is not the source (R37); **(`--strict-done`)** every `DONE` row carries an `https://` URL, a CI run-id or `origin/<ref>` — a local commit hash is not proof (R36).
The agent pastes this exit code and output as the last line of the turn.

---

## What the human does (30 seconds)

1. Glance at `SENTENCES: N` vs. `REQ-NN`. If the ledger has far fewer REQs than sentences, reply with one line: **"ledger short — redo Step 1."** Do not read further.
2. At the end, glance at the closure table for any `[Q]` not `ANSWERED`. Reply: **"REQ-xx unanswered."**
3. Nothing else. You never re-read your own message to check whether it was read.

---

## Why this beats "please read everything carefully"

| Prose instruction | This protocol |
|---|---|
| "Read every word" — unverifiable | `SENTENCES: 14` / `REQ-09` — visibly short |
| "Answer all my questions" — agent decides what counts as a question | Every `?` / interrogative is forced into a `[Q]` row that must be `ANSWERED` |
| "Don't summarise" — agent summarises anyway, you find out later | Verbatim quotes in the ledger; a paraphrase is a visible violation |
| "Don't forget the constraint I mentioned" — forgotten next turn | `[RULE]` REQs are copied into `ANCHORS.md` the same turn |
| You re-read 2,000 words to check | You count rows |

---

## Session-start addendum (added to AGENT_HARD_RULES checklist)

```
[ ] First output of the first turn is a req-ledger block. No tool call precedes it.
[ ] Last output of every turn is a req-closure block + req_coverage.py exit code.
```

## Known limits (stated so nobody over-trusts this)

- The agent can still write a REQ and then do it badly. This protocol guarantees **coverage**, not **quality**. Quality is what the consultant reviews and CI gates check.
- The agent can miscount `SENTENCES`. That is why the human glances at the ratio, not the absolute number. A ledger of 9 REQs for a 3-paragraph message is obviously short regardless of what `SENTENCES` says.
- Very long messages (>40 sentences) should be split by the human into numbered parts; the protocol scales linearly but human verification does not.

*Added in Round 5 by the Genspark consultant, in response to the user's explicit requirement that no character, word or line of a message may be dropped.*
