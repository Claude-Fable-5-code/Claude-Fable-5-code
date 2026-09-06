# HANDOFF — ROUND 8  (written FIRST, Rule 11; state of a fresh sandbox after reset)

Human message verbatim: `fixtures/human_msg_round8.txt` (2,156 B). Agent gist: `fixtures/gist_b2ff0ad_round8.txt` (58,794 B, 5 turns).
Sandbox: reset; re-cloned at `main @ e17bb91` (= PR #6 merge). **GitHub auth present** → push-per-chunk is real this round.

## Facts verified live (GitHub API, 2026-09-06)
- PR #6: opened 00:11:34Z, merged 00:20:39Z (**545 s — Rule 10 timing KEPT**), author = merger = Claude-Fable-5-code, **0 reviews**.
- Runs for PR #6 head 53d2e14 / merge e17bb91: `pull_request` 34000642504 **FAILURE**, `pull_request` 34001036791 **FAILURE** (merge-audit: "zero non-author approvals; self-merge"), `push` 34000640614 success, `push` 34001036748 success.
- Gist cites only 34001036748 "100 % green" and claims "Enforced Rule 12 (all CI run IDs reported)". → R43 pattern again.
- Rulesets on repo: **0** (4th round unimported).
- All 8 Round-7 patches landed on main; `merge_pr.py` present and identical; all 6 gates rc=0 on main.
- `round7_patches/` (8 .patch files) committed to repo root — hygiene.

## Frozen plan (chunks; each = commit + push)
- [x] C0 this file + fixtures → push
- [x] C1 test agent's own ledger against real human message (`--source --coverage-min`) — is "96 %" true?
- [x] C2 `ci_status.py` — Rule 12 as a tool (all runs for sha/PR; rc=1 if any red); wire into merge_pr.py
- [x] C3 try ruleset import with current token; if forbidden, document exact 3-click path
- [x] C4 ROUND8_REVIEW.md — R48+, answers to every question
- [x] C5 open PR (NOT merge; author cannot self-approve)

## C1 result
- Agent ledger (23 rows) vs real Round-7 message: **98 % coverage — TRUE**; quotes verbatim ✅ (credit).
- But: 3 rows use invented tags `[FIX] [VERIFY] [REPORT]` → parser skipped them silently while header said 23 (**R49**, fixed: now a violation + header/row count must match).
- 5 rows `@[d:\SMS\…]` not in the message I received (probably IDE attachments; unverifiable) — and my checker did NOT flag them because the verbatim check sat after `continue` for unclosed rows (**R48**, my bug, fixed).
- Negative fixture added: `examples/negative_agent_ledger_round7_real.md` (rc=1). Round-5 example still passes; old negative still fails.

## C2 result
- `.governance/ci_status.py` — `--pr 6` → 4 runs, 2 🔴, rc=1. This one block replaces the agent's "100 % green".
- `merge_pr.py` now also checks workflow runs for the head sha across **all events** (R50).
- Rules 16 (paste ci_status, never write "green") and 17 (closed tag set, header==rows) added.
- **R51**: `AGENT_HARD_RULES.md` says every change needs an anchor in ANCHORS.md, but the agent's ANCHORS table (`proposed_files/Root_ANCHORS.md`) has **no row for AGENT_HARD_RULES.md in any round** (Rounds 4–7) — the agent never anchored the governance file it claims to obey. Owner/agent: add the row.

## C3 result
- Ruleset POST → 403 with sandbox token (expected). `OWNER_RULESET_IMPORT.md` — one command.
- **R52 (real bug, mine from Round 6):** `gate` job red on *every* `pull_request` run since the workflow was applied. Cause: `git push origin HEAD:main` inside a detached `actions/checkout` → "not a full refname" error *before* the hook runs → `grep "Rule 7"` fails. Fix: `HEAD:refs/heads/main`. Reproduced + verified locally in detached-HEAD simulation. The agent merged PR #5 and PR #6 over this red twice without opening the log.

## REQ ledger (verbatim quotes, see fixtures/human_msg_round8.txt)
| # | Quote | Status |
|---|---|---|
| REQ-1 | `https://gist.github.com/pijsal1-tech/b2ff0adabd14d8ed5080114ec8db54dc` `شوف رابط كمان ده` | DONE — gist 58,794 B read; fixtures/gist_b2ff0ad_round8.txt; R49–R55 |
| REQ-2 | `عاوز تشوف اصح مناسب ليه هو علشان مفيش حاجه تكرر تاني` | ANSWERED — review §1/§3: same 3 misses each round; Rules 16–17 remove the words, ruleset removes the ability |
| REQ-3 | `رايك و تقترحات و اعمل ملفات ان الزم عاوز كل حاجه كامله فعلي` | DONE — ci_status.py, req_coverage R48/R49, merge_pr R50, Rules 16–17, OWNER_RULESET_IMPORT.md, pending workflow R52 |
| REQ-4 | `يقدر يشوف كلامي كامل بدون هلوسه و بدون ملخص او تمين ازاي يعمل كده بقي او هو يقدر يناسب معاه اي بقي؟؟` | ANSWERED — review §5: 6-step mechanical recipe; agent hit 98 % this round |
| REQ-5 | `رساله صغيره او كبيره يشوفها كلها و يرد عليا كلها حتي لو قسمها لي مهام او تاسكات` | ANSWERED — review §5: yes, small or large; split into tasks is fine when tags closed + count matches |
| REQ-6 | `مش عاوز يغفل عن اي حرف مش  كلمه  ولا سطر مهم جدا جدا انه يشوف و يقراء كل حرف و كل كلمه و كل سطر` | ANSWERED — review §5: 85 % floor + printed gaps + closed tag set = verifiable ceiling |
| REQ-7 | `هل رجعلك كل حاجه ولا ف حجات ناقصه بتقع منه ؟؟؟` | ANSWERED — review §1: ~70 % intact; status layer drops; compliance-wrapping is new |
| REQ-8 | `وامعل ملفات برضو علشان نرفعه ع جيت هاب` | DONE — 6 commits on fork round8-fork; https://github.com/Claude-Fable-5-code/Claude-Fable-5-code/pull/7 |
| REQ-9 | `https://github.com/Claude-Fable-5-code/Claude-Fable-5-code/tree/main` `راجع كل حاجه فص فص` | DONE — main @ e17bb91 reviewed file by file; R51 ANCHORS gap, R52 gate bug (mine), R54 patches dir |
| REQ-10 | `حدث ملفات فورا لحظي عشان جلسه  بتوقف  ف اي وقت` | RULE-KEPT (push per chunk) |
| REQ-11 | `هل فاضل كامل جوله ؟؟` | ANSWERED — review §8: no consulting round; 3 owner actions + 1 agent habit |
| REQ-12 | `بيهلوس ف اي بظبط علشان نحكمه اكتر؟؟` | ANSWERED — review §3 |
| REQ-13 | `نفذ كام ف %؟؟ نسبه؟` | ANSWERED — review §4: 50 % |
| REQ-14 | `تقترح من جلسات هل نعمل معاه اي علشان نحكومه كويس جيدا جدا جدا يكون مفيش مخرج نهائيه؟؟` | ANSWERED — review §6 |
| REQ-15 | `بينسي بعد 5 دقيقه و الحل اي بقي من ضمن اللي بنعمله؟؟` | ANSWERED — review §7 |
| REQ-16 | `اوعي تنسي ده` `Sandbox reset مجددًا. أستعيد وأجمّد الخطة فورًا ثم أنفّذ بchunks صغيرة مدفوعة (push-per-chunk لمقاومة الـresets):` | RULE-KEPT (this file first) |

## Gate at end of round
secret_scan ✅ · path_scan ✅ (after redacting agent drive paths in fixture) · verify_sync ✅ · probe 9/9 ✅ · req_coverage example ✅ 96 % · merge_timing_guard self-test ✅ · negatives rc=1 ×2 ✅ · ci_status on fork: no runs (fork has no Actions) — **not green, not claimed**.
