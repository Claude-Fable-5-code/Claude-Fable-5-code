# FULL READ PROTOCOL — every character, every line, every question

**Tier:** T0. Applies to every AI agent turn that responds to a human message on this project.
**Enforced by:** `python .governance/req_coverage.py` (mechanical) + the human counting rows (30 seconds).

---

## The honest premise

You cannot make a language model "read harder." It already sees every token. What goes wrong is downstream: it **acts on a compressed version** of what it saw — merging two requests into one, treating a question as a statement, answering the loud part and dropping the quiet part.

So this protocol does not ask the agent to read carefully. It asks the agent to **produce an artifact that is impossible to produce without having processed every sentence**, and it makes that artifact **countable** so the human can verify coverage in seconds without re-reading their own message.

---

## Step 0 — Save, then detect intent (Round 9)

1. `fixtures/human_msg_<n>.txt` ← the human message, byte-for-byte, before anything else (Rule 14).
2. `python .governance/intent_gate.py detect fixtures/human_msg_<n>.txt`
   - `MODE: PLAN-ONLY` → the whole turn is one ` ```plan-only ` block (UNDERSTOOD / I WILL / I WILL NOT / WAITING FOR). Zero tool calls that change state. Stop. (Rule 19)
   - `MODE: ACT` → continue to Step 1.

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

## Step 1b — Size does not matter; the ledger does

"Small or large message, see all of it" — the mechanism is identical. A 3-word message produces a 1-row ledger. A 3,000-word message produces N rows and `req_coverage.py --full` prints every fragment — down to one character — that no row or LEFTOVER line quotes (Round 10; `--coverage-min 85` is retired). The agent does not decide what is important; the checker decides what is missing.

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

## Step 1c — Splitting a long message is allowed; dropping any of it is not (Round 10, R69)

"حتى لو قسمها لي مهام او تاسكات" — a long message may be split into many REQs across several turns, but the *union* of the quotes in the first ledger must still be the whole file: run `req_coverage.py --full` on the ledger before doing anything. Non-requirement text is declared, not ignored: `LEFTOVER [SEPARATOR] «""»`, `LEFTOVER [URL] «https://…»`, `LEFTOVER [AGENT-ECHO] «Sandbox reset مجددًا.»`. If the tool prints an unaccounted fragment, the ledger is redone — the agent never decides what was unimportant.

## Step 0b — Every tool block goes through `attest.py run` (Round 10, R63)

`ci_status`, `remote_proof`, `intent_gate`, `req_coverage`, `merge_pr` are never pasted directly. `python .governance/attest.py run -- python .governance/<tool> …` prints the output plus an `ATTEST` footer; the block is pasted with its footer. The human verifies with `attest.py verify <turn> --live`.

## Step 1b — Character coverage (Round 7, R47; superseded by Step 1c in Round 10)

`--source` proves every quote exists in the message. It does **not** prove the message was consumed: a ledger of 3 real quotes from a 20-sentence message passes `--source`. `--coverage-min P` closes that hole: the checker marks every non-space character of the message that lies inside some quote and fails if fewer than P % are marked, **printing the exact uncovered spans**. Floor for this project: **85 %**. Tags `[CTX]` exist precisely so filler sentences can be quoted without inventing a task for them.

Operational rule: the human message is saved byte-for-byte to `docs/…/fixtures/human_msg_<round>.txt` **before** the ledger is written (it is the `--source`). The agent never types a quote from memory — it copies from that file. Round 7 note: the consultant itself produced a quote from memory that belonged to a *different* message and was caught by this check.

## Step 4 — Mechanical check

```
python .governance/req_coverage.py <turn.md> --strict-done --source <human_message.txt>
```
Exit 0 only when: every `REQ-nn` in the ledger has a closure row; every `[Q]` is `ANSWERED` or `BLOCKED` (never `DEFERRED`, never `DONE`); `UNMAPPED` is `none`; no closure row exists without a ledger row; **(`--source`)** every ledger quote occurs verbatim in the human's message — save the message to a file first, the agent's memory of it is not the source (R37); **(`--strict-done`)** every `DONE` row carries an `https://` URL, a CI run-id or `origin/<ref>` — a local commit hash is not proof (R36).
The agent pastes this exit code and output as the last line of the turn.

## Step 4b — Prose check, after the turn is drafted and before it is sent (Round 11, R71)

```
python .governance/attest.py verify <turn.md> --live      # blocks are real, not stale-success
python .governance/claim_check.py <turn.md>               # sentences do not contradict the blocks
```
Round 11: all 8 blocks were genuine and the prose above them said the opposite of what they printed. Save the draft to a file, run both, paste both outputs as the final block of the turn. If `claim_check` lists a sentence, delete or invert the sentence — never touch the block.

---

## Step 0a — Mirror before anything, when asked (Round 12, R83, Rule 27)

```
python .governance/intent_gate.py detect fixtures/human_msg_<round>.txt
```
If it prints `MODE: CONFIRM-FIRST`, the turn is a single ```mirror block and nothing else — no ledger yet, no tool call, no plan. Quote the human's sentences verbatim under `UNDERSTOOD:`, one reading per sentence, `QUESTION:` for what the text cannot settle, `WAITING FOR: تمام`. Only the next turn (after the human's confirmation) proceeds to Step 1.

## Step 2b — Read the whole file before naming a cause (Round 12, R84, Rule 28)

```
python .governance/attest.py run -- python .governance/read_proof.py index <file>      # paste the block
python .governance/read_proof.py check <turn.md>                                        # before sending
```
No "the bug is / السبب / الخطأ في" about a file that has no live `read_proof` block in the same turn. `check` also fails a proof whose sha no longer matches the file (you read an older version) or a proof of a different file than the one you diagnose.

## Step 4c — Never type a verdict (Round 12, R81, Rule 29)
`claim_check.py` C7: any `✅/⛔ <tool>:` line or `MODE:` line outside an attested block fails the turn. The only way to have a verdict in the turn is `attest.py run -- python .governance/<tool>.py …` and pasting what it printed, footer included.

## What the human does (30 seconds)

1. Glance at `SENTENCES: N` vs. `REQ-NN`. If the ledger has far fewer REQs than sentences, reply with one line: **"ledger short — redo Step 1."** Do not read further.
2. At the end, glance at the closure table for any `[Q]` not `ANSWERED`. Reply: **"REQ-xx unanswered."**
3. Round 11: `python .governance/claim_check.py <its-reply.md>` — one command. If it prints 🔴, reply with the line it printed. You do not need to read the reply.
3b. Round 12: if you asked it to confirm understanding first, `python .governance/intent_gate.py verify <its-reply.md> --human <your-msg.txt>`; if it named a bug, `python .governance/read_proof.py check <its-reply.md>`. Either prints ⛔ → paste that line back.
4. Nothing else. You never re-read your own message to check whether it was read.

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

## Step 0c — Plan file first, export after every chunk (Round 13, R89, Rule 33)
```
# before any tool work:   docs/…/PLAN_ROUND<N>.md with the frozen chunk list, then commit
# after every chunk:      git commit && sh .governance/export_bundle.sh   → upload → URL into the plan (next commit)
```
No URL, no tick. `setup_github_environment` first; if no token, do not try `git push` — export.

## Step 2c — Edit claims carry a diff (Round 13, R86, Rule 31)
```
python .governance/attest.py run -- python .governance/edit_proof.py show <path> [<path>…]    # paste the block
```
"عدّلت / fixed / edited <file>" without an `edit_proof` block for that file (state ≠ UNCHANGED, sha = disk) fails `edit_proof.py check`.

## Step 2d — Admissions are recorded (Round 13, R85, Rule 30)
```
python .governance/attest.py run -- python .governance/mistakes.py record --round <N> --rule <R> "<one line>"
```
Then the prose may say "I was wrong". `mistakes.py check <turn>` fails an admission with no row.

## Step 4d — Self-review with six questions (Round 13, R87, Rule 32)
```self-review
Q1 attested:   ✅/❌  evidence: sha256=<footer sha of a block in this turn>
Q2 prechecked: ✅/❌  evidence: sha256=<footer sha of the precheck block>
Q3 skipped:    <check name + why>  | none          (none only with ≥ 3 tool families in the turn)
Q4 pleasing:   «<verbatim sentence from this turn's prose>» | none
Q5 re-read:    ✅/❌  missed: «<verbatim from the human message>» | none missed
Q6 remote:     ✅/❌  evidence: <remote_proof REMOTE> | none — <why>
```

## Step 0d — State open at the start, state close at the end (Round 14, R90, Rule 35)
```
python .governance/attest.py run -- python .governance/state_gate.py open [--ack-drift]      # FIRST block of the turn
python .governance/attest.py run -- python .governance/state_gate.py close --write --tag "[ROUND<N>-C<k>]" --last "…" --next "…"   # LAST block, before precheck
```
`precheck.py` step 0 (`state_gate check`) fails a turn whose first attested block is not `state_gate open` or whose last is not `state_gate close` on the same head. Pre-commit refuses staged code without a staged `Root/ai_state.json`.

## Step 2e — Edits stay inside the promised lines; no placeholder code (Round 14, R92/R93, Rule 37)
```
python .governance/attest.py run -- python .governance/edit_proof.py show <file> --scope A-B   # hunks in HEAD numbering; OUT-OF-SCOPE ⇒ exit 1
python .governance/attest.py run -- python .governance/mock_scan.py --staged                   # also runs in pre-commit and CI
```

## Step 2f — A repeated rule needs an ESC row (Round 14, R91, Rule 36)
```
python .governance/attest.py run -- python .governance/mistakes.py recurrence                  # precheck step 6b
python .governance/attest.py run -- python .governance/mistakes.py record --round <N> --rule <R>-ESC "<the mechanism that prevents the third>"
```

## Step 5 — Precheck, then send (Round 13, R88, Rule 34)
```
python .governance/attest.py run -- python .governance/precheck.py <turn.md> --source <human.txt>   # paste table; its sha → Q2
```
Stops at the first red step. Fix, re-run, paste the green table. Only then send.

## Session-start addendum (added to AGENT_HARD_RULES checklist)

```
[ ] First output of the first turn is a req-ledger block. No tool call precedes it.
[ ] Last output of every turn is a req-closure block + req_coverage.py exit code.
[ ] Round 12: intent_gate detect ran on the human message; CONFIRM-FIRST → mirror block only. No cause named without a read_proof block. No verdict line typed.
[ ] Round 13: PLAN_ROUND<N>.md committed before any tool work; MISTAKES.md read; every chunk row has an export URL; precheck table pasted before sending; self-review has a ❌ or a REMOTE proof.
[ ] Round 14: first block is `state_gate open`, last is `state_gate close --write`; `mistakes.py recurrence` green (or an -ESC row written); every edit claim with a line range carries `--scope`; `mock_scan --staged` green before every commit.
```

## Known limits (stated so nobody over-trusts this)

- The agent can still write a REQ and then do it badly. This protocol guarantees **coverage**, not **quality**. Quality is what the consultant reviews and CI gates check.
- The agent can miscount `SENTENCES`. That is why the human glances at the ratio, not the absolute number. A ledger of 9 REQs for a 3-paragraph message is obviously short regardless of what `SENTENCES` says.
- Very long messages (>40 sentences) should be split by the human into numbered parts; the protocol scales linearly but human verification does not.

*Added in Round 5 by the Genspark consultant, in response to the user's explicit requirement that no character, word or line of a message may be dropped.*
