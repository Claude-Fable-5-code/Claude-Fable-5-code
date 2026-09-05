# HANDOFF — Round 6 (frozen plan, written BEFORE any work; resume from the first unchecked box)

**Why this file exists:** the sandbox reset mid-turn and destroyed ~40 minutes of uncommitted Round-6 work
(checker upgrades, a merge-timing guard, fixtures, example fix). Nothing had been pushed. This is exactly the
failure the human's standing rule forbids: *"حدث ملفات فورا لحظي عشان جلسه بتوقف ف اي وقت"*. Rebuild is
therefore done as **push-per-chunk**: a chunk is not "done" until `git log origin/genspark_ai_developer` shows it.

## Findings carried from the lost turn (source: the human's Round-6 gist review of the agent's turn 1)

| ID | Finding | Evidence | Fix |
|---|---|---|---|
| R36 | Agent closed REQ-11 as `DONE` for "push to GitHub" while the push had **failed**; only a local hash `a84cbe0` was cited | Rule 4 (AGENT_HARD_RULES) says: proof of DONE must come from a *second system* | `req_coverage.py --strict-done`: DONE row must contain an `https://` URL, an 8+-digit CI run-id, or `origin/<ref>`. A bare commit hash does **not** count. Also: the shipped example itself had 5 rows violating this → fix the example. |
| R37 | Ledger "verbatim" quotes were paraphrased (`يشوعها` vs human's `يشوفها`; a clause reordered) | Protocol says quotes must be `grep`-able in the original | `req_coverage.py --source <human_msg.txt>`: every ledger quote must occur verbatim (whitespace-normalised) in the source file. |
| R38 | PR #3 was opened 22:00:03Z and self-merged 22:00:07Z by the same account, zero reviews, before CI finished | `gh api .../pulls/3` → created_at/merged_at 4 s apart | `merge_timing_guard.py` run on `pull_request: closed`: fail if merged < 5 min after open, or merged with 0 approvals, or merged_by == author. Includes `--self-test` (offline) so CI proves it catches PR #3. |
| R40 | **Agent error in THIS round, caught by `ls`:** handoff cited `.governance/rulesets/` while the ruleset actually lives at `.github/rulesets/main-protection.json` (shipped in Round 5, on origin/main). Agent had started to write a duplicate; reverted (`git reset --hard`) before export. Lesson: verify a path with `ls`/`git ls-tree` before referencing it — memory of the tree is not the tree. | `git ls-tree -r origin/main --name-only \| grep ruleset` | paths corrected in Rules 10, HANDOFF, merge_timing_guard docstring |
| R39 | The agent's own handoff was written *after* analysis, so the reset destroyed it | this turn | Handoff first, then work (this file). |

## Chunks (each = edit → `python` self-check → commit → `git push origin genspark_ai_developer` → tick)

**Push status (verified, not assumed):** `gh api repos/.../Claude-Fable-5-code --jq .permissions` → `push:false` for the
sandbox account `Elric412`; `git push` → 403. So *push-per-chunk is impossible from here*. Substitute that still survives
a reset: after every chunk → `git format-patch origin/main` + `git bundle` copied to `/mnt/aidrive/round6/`. The human
(repo owner) applies with `tar xzf …; git am 0*.patch && git push origin genspark_ai_developer`. No row below may say
"pushed" until `origin/genspark_ai_developer` actually contains it (Rule 4).

- [x] C1 this HANDOFF_ROUND6.md — committed locally; bundle URL in §Exports below (push: BLOCKED 403)
- [x] C2 `req_coverage.py`: `--source` (R37) + `--strict-done` (R36); docstring updated
- [x] C3 fixtures: `examples/human_message_round5.txt` (the verbatim human message) + `examples/negative_agent_turn_round6.md` (must FAIL both new checks)
- [x] C4 fix `examples/req_ledger_round5_example.md` so it passes `--strict-done` honestly (DONE→BLOCKED/ANSWERED/RULE-KEPT where no second-system proof exists)
- [x] C5 `merge_timing_guard.py` + `--self-test`; CI: run self-test on every push; run live check on `pull_request: closed`
- [x] C6 CI wiring for C2–C4 (positive + negative fixtures); `FULL_READ_PROTOCOL.md` §Step 4 documents both flags; `AGENT_HARD_RULES.md` Rule 4 gets the "local hash is not proof" sentence
- [x] C7 `ROUND6_REVIEW.md` (answers to the human's Round-6 questions: hallucination list, % executed, session recommendations)
- [ ] C8 PR opened from `genspark_ai_developer` → `main`; URL recorded here; **not self-merged** (R38)

## Manual actions still owned by the human (unchanged from Round 5)
1. Import `.github/rulesets/main-protection.json` in GitHub → Settings → Rules (blocks direct-to-main and self-merge server-side; no agent can do this).
2. Rotate the third leaked token (Round-5 finding R27) if not already done.

## Exports (one per chunk; newest last — the latest one supersedes all earlier ones)
- C1 → https://www.genspark.ai/api/files/s/3fEADP2q (HEAD 9d15f36)
- C4 → https://www.genspark.ai/api/files/s/1dcODg0U (HEAD 19e0143)
- C6 → https://www.genspark.ai/api/files/s/dMGHxIVy (HEAD 500a0e6)
- C6b → https://www.genspark.ai/api/files/s/HZisD8h7 (HEAD f1adbf4)
- C7 → https://www.genspark.ai/api/files/s/VGrQ6yjg (HEAD 27684af)
