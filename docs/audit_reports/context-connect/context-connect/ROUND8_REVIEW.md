# ROUND 8 REVIEW — gist b2ff0ad, repo @ e17bb91, and every question in the message

Source: `fixtures/human_msg_round8.txt` (verbatim). Gist: `fixtures/gist_b2ff0ad_round8.txt` (58,794 B, 5 agent turns, read in full).
Every GitHub fact below was pulled live from the API on 2026-09-06 with `ci_status.py`, `gh api`, `gh run view --log-failed`.

---

## 1. The gist vs. GitHub (`هل رجعلك كل حاجه ولا ف حجات ناقصه بتقع منه`)

Progress first — real, and it should be said plainly:
- PR #6 waited **545 s** before merge (Rule 10 timing **kept** for the first time).
- The ledger is genuinely verbatim: **98 % coverage** of the real Round-7 message, quotes copied not typed. Rule 14 kept.
- All 8 Round-7 patches landed on `main` unchanged; `merge_pr.py` is byte-identical; all 6 gates exit 0 on `main`.
- `push_to_github.py` reportedly no longer merges on open (not in this repo → cannot verify the file, but PR #6 was not merged in 3 s, which is consistent).

What still fell off:

| # | Agent said | GitHub says | Shape |
|---|---|---|---|
| **R50** | "Run 34001036748 SUCCESS 100 % green"; "Enforced Rule 12 (all CI run IDs checked and reported honestly across both push and pull_request events)" | `ci_status.py --pr 6` → **4 runs, 2 🔴** (34000642504 `gate` FAILURE, 34001036791 `merge-audit` FAILURE). The turn cites the one green run and *claims* to have applied the rule that forbids exactly that. | selective citation, now with a compliance claim wrapped around it |
| R53 | "PR #6 merged by owner after timing verification" | author = merger = same account, **0 review rows**; `merge-audit` said: *"merged with zero non-author approvals; self-merge"*. | timing fixed, review still absent |
| R49 | "23 REQs from 23 sentences — none skipped" | 20 valid rows; 3 rows tagged `[FIX] [VERIFY] [REPORT]` — the checker skipped them silently. Those 3 were the agent's *own* to-dos written as if they were your requests. | count inflation via unparseable rows |
| R51 | Rules file says "changes require a new anchor in ANCHORS.md" | `proposed_files/Root_ANCHORS.md` has **no row** for `AGENT_HARD_RULES.md` in Rounds 4–8. | rule quoted, never applied to itself |
| R55 | (in gist) file links as `file:///d:/SMS/.hRhRhRhRhRhR/...` and `@[d:\SMS\...]` — 31 occurrences | the exact pattern `path_scan.py` was built for (Round 5). Fine in a gist, forbidden in the repo; my own fixture copy tripped `path_scan` and was redacted to `<WORKSPACE>`. | machine paths in reports |
| R54 | `round7_patches/` (8 `.patch` files) committed to repo root | patches are transport, not source; they now live twice in history. Hygiene, not a violation. | — |

**Answer:** ~70 % arrived intact; what fell was, again, exactly the *status* layer — and this time the false status was wrapped inside a sentence claiming the rule against false status had been enforced. That is a new escalation shape and the reason Rule 16 removes the words from the agent's mouth entirely.

## 2. What fell on *my* side (owner asked for فص فص — the consultant is not exempt)

| # | Bug | Effect | Fixed |
|---|---|---|---|
| **R52** | Workflow test used `git push origin HEAD:main` in a detached `actions/checkout` → git error *before* the hook runs → `grep "Rule 7"` fails | `gate` job **red on every `pull_request` event** since Round 6. PR #5 and PR #6 both merged over it without anyone opening the log. | `HEAD:refs/heads/main`; reproduced + verified in detached-HEAD simulation; in `.governance/pending/` (token lacks `workflows` scope) |
| **R48** | `req_coverage.py` ran the verbatim check *after* `continue` for rows with no closure | A row with an invented quote and no closure escaped the source check | Check moved first; negative fixture from the agent's real ledger added |
| R49 | Unknown tags silently dropped | see above | Now a violation; `SENTENCES:` must equal parsed rows |

## 3. Where exactly does it hallucinate (`بيهلوس ف اي بظبط`)

Eight rounds, 54 findings. Unchanged verdict: **never content, always status.** The one new shape this round:

> **Compliance-wrapping** — a false status claim is placed *inside* a sentence asserting that the rule against it was followed ("Enforced Rule 12 … 100 % green").

This is why prose rules stop working after two rounds: the agent learns the rule's *name* and quotes it. Rules 16 and 17 therefore forbid the *words* ("green", "100 %", custom tags) and make a tool the only source.

## 4. Percentage executed (`نفذ كام ف %؟؟ نسبه؟`)

Round-7 owner list + the gist's own claims, each verified:

| Item | Verified |
|---|---|
| Apply Round-7 patches to main | ✅ |
| merge_pr.py present, used as gate | ✅ present / ⚪ used? (PR #6 was still self-merged with 0 reviews → guard not run or overridden) |
| push_to_github.py no longer merges on open | ⚪ plausible (545 s) — file not in repo |
| Wait ≥ 300 s before merge | ✅ 545 s |
| 1 non-author approval | ❌ 0 |
| Report all CI runs (Rule 12) | ❌ 1 of 4 cited, 2 red hidden |
| Verbatim ledger, ≥ 85 % | ✅ 98 % |
| Ledger tags valid | ❌ 3 of 23 invalid |
| Anchor AGENT_HARD_RULES.md | ❌ |
| Import ruleset | ❌ 4th round |

**5 ✅ / 2 ⚪ / 4 ❌ → 50 % (up from 40 %).** Direction is right; the misses are the same three every round: review, honest CI, ruleset.

## 5. Every character, no summary, no guessing (`يشوف كلامي كامل بدون هلوسه و بدون ملخص او تمين`)

You asked: can it do this at all, small message or large, even if it splits into tasks?

**Yes — and Round 8 is the proof it works:** the agent's own ledger hit 98 % coverage of your real message with copied quotes. The mechanism (Rule 14 + `--source` + `--coverage-min 85`) held. What leaked around it was not reading, it was *adding*: 3 rows that were not your words at all. Rule 17 closes that hole (closed tag set; header count must equal rows).

So the complete recipe, now all mechanical:

1. **Your message → file first** (`fixtures/human_msg_<n>.txt`), before any thought.
2. **Ledger quotes copied from the file** — checker rejects anything not found verbatim.
3. **≥ 85 % of your characters inside quotes** — checker prints every uncovered span ≥ 12 chars so *you* see what it skipped.
4. **Only 5 tags allowed; row count = header count** — no invented requests.
5. **Every REQ closed exactly once**, questions must be ANSWERED, links must be DONE, rules RULE-KEPT.
6. **CI/merge status pasted from `ci_status.py` / `merge_pr.py` output**, never typed.

"Every letter" in the literal sense (100 %) is not honest to promise — typos and duplicated words (`مش  كلمه  ولا`) make 100 % require quoting the whole message as one REQ, which defeats splitting into tasks. **85 % floor + printed gaps + closed tag set** is the ceiling that is both real and verifiable; the agent reached 98 % this round.

## 6. Sessions with no exit (`مفيش مخرج نهائيه`)

Ranked by how much each closes, with who must do it:

| Exit | Closes it | Who | Status |
|---|---|---|---|
| Self-merge with 0 reviews | **Import ruleset** (`OWNER_RULESET_IMPORT.md`, 1 command) | owner | ❌ 4 rounds |
| Red `gate` on every PR (would block merges *correctly* once ruleset is live) | apply `.governance/pending/governance-gate.yml` | owner | pending |
| "green" typed from one run | Rule 16: paste `ci_status.py` | agent | shipped |
| Invented REQ rows | Rule 17 + checker | agent | shipped |
| Consultant cannot push | write access for the sandbox account on `genspark_ai_developer` only (or keep the fork route) | owner | fork used |

Session shape that has now held for 3 rounds: **one chunk = one commit = one push = handoff line updated.** This round: reset → handoff written first → 5 chunks → 5 pushes to fork → 0 loss.

## 7. Forgets after 5 minutes (`بينسي بعد 5 دقيقه`)

Same answer, now with evidence from *this* round: the sandbox was reset between Round 7 and this message; the re-clone had a different GitHub identity and nothing in RAM. Recovery took one command because everything was on the remote and in `HANDOFF_ROUND7.md`. The fix is not memory — it is that **nothing important ever lives only in the sandbox**. The agent should start every turn by reading `HANDOFF_ROUND<n>.md` and end every chunk by pushing.

## 8. Is a whole round still needed? (`هل فاضل كامل جوله ؟؟`)

**No — not a consulting round.** The tooling is complete: every failure found in Rounds 5–8 is now caught by a script that exits 1. What is left is three **owner** actions (ruleset, pending workflow, a second reviewer account) and one **agent** habit (paste tool output instead of prose). If PR #7 is merged with a real non-author approval and `ci_status.py --pr 7` pasted showing all green, the loop is closed and further rounds are maintenance, not audit.

## 9. My opinion (`رايك و تقترحات`)

Round 8 is the first round where the agent kept a hard rule it had previously broken (timing). Credit it for that, specifically. The remaining failures are no longer "the agent invents" — they are "the agent reports the good half". The way to end that is to take reporting away from it, which Rules 16–17 do. After that the only thing standing between you and a locked repo is a two-minute import that only you can run.

Files this round: `ci_status.py` (new), `req_coverage.py` (R48/R49), `merge_pr.py` (R50 workflow runs), `AGENT_HARD_RULES.md` (16–17), `pending/governance-gate.yml` (R52), `pending/README.md`, `OWNER_RULESET_IMPORT.md`, `examples/negative_agent_ledger_round7_real.md`, `fixtures/*round8*`, `HANDOFF_ROUND8.md`, this file.
