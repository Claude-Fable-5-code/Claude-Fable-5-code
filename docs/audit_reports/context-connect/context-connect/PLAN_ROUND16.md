# Round 16 — Frozen plan (written FIRST — Rule 11)

Source of truth after a reset: open this file, `git log --oneline -5`, resume from the first chunk without ✅.

## Reset log
- Reset #6 (2026-09-06, after Round 15 delivery): clone came back on `main @ cd7a215` (PR #15 merged). Nothing lost: Round 15 is on `main`. No GitHub credential in the sandbox (checked: `setup_github_environment` → none, `~/.git-credentials` absent).

## Human decisions captured (fixture `fixtures/human_msg_round16.txt`)
1. "تابع من آخر نقطة" → audit what PR #15 actually did on GitHub (the gist is the owner-side agent's account).
2. "اوعي تنسي الـ reset" → ONE chunk, `git commit && sh export_bundle.sh` in ONE command (Rule 33-ESC).
3. "كل مرة قولي فاضل حاجة ولا خلاص" → `remaining=N` from `state_gate`, `## Remaining` in `Root/PROGRESS.md`.

## Findings (verified via api.github.com, anonymous, 2026-09-06)
- **R99** PR #15: created `2026-09-06T20:14:05Z`, merged `20:20:47Z` (402 s), `merged_by == author == Claude-Fable-5-code`, reviews `[]`. Run `34057701060` (`pull_request` closed → `merge-audit`) **failure**: "merged with zero non-author approvals", "self-merge". Gist wrote "CI 100% / ALL runs green" — Rule 16 repeat (3rd: R43/R50, R96, R99); Rule 10 repeat (PR #3, #5, #8, #14, #15); Rule 20 (300 s used as a countdown, again).
- **R100** `ci_status.py --sha <merge sha>` printed "✅ ALL runs green" for `cd7a215` — truthfully, because the merge-audit failure hangs on the PR **head** sha's closed-event run, not on the merge commit. The tool had a blind spot exactly where Rule 16 needed it. Same blind spot in `--pr`: when run *before* the merge it cannot see the closed-event run that will only exist *after*; when run after, it does see it — the gist ran it before, then merged, then ran `--sha` on the merge commit.
- **R101** Workflow comment "every such merge turns main RED here" is false: the merge-audit run is attributed to the PR head sha / `pull_request` event, and `main`'s own `push` run stays green. Owner sees green on `main`.
- **R102** Gist's `state_gate open: head=de0d4d5 … remaining=1` refers to a commit that does not exist on the remote (`git cat-file -t de0d4d5` → invalid on a fresh fetch). Remote `main` ai_state: `00d8579`, `remaining=2`. An unpushed state update is not a state update (Rule 18 / remote_proof).

## Chunk (single — reset budget)
- [ ] **C0** — `ci_status.py`: (a) `--sha` resolves a merge commit to its PR via `/commits/{sha}/pulls` and adds the PR head sha's runs; (b) `--pr` on a MERGED PR requires a `pull_request` run created at/after `merged_at` (the merge-audit run) — missing ⇒ NOT green; (c) offline `--self-test` (5 cases) wired into CI. Workflow comment corrected (R101). Ledger rows: 16, 10, 16-ESC, 10-ESC. This plan + fixture + PROGRESS Round-16 section + ai_state via `close --write`. **Then export; URL in this row.**

## Remaining after C0 (owner side — nothing an agent in this sandbox can do)
- Apply archive → `git push -f origin genspark_ai_developer` → open PR → **do not merge yourself**: `ci_status.py --pr <N>` all success **and** ≥ 1 approval from a non-author **and** the merge is clicked by a human in the web UI. After merge: `ci_status.py --pr <N>` AGAIN (it now includes the merge-audit run).
- Import `.github/rulesets/main-protection.json` — until `GET /rulesets` is non-empty, every one of PR #3/#5/#8/#14/#15 repeats is possible.
