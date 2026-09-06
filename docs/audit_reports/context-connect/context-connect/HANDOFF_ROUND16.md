# HANDOFF — Round 16 (post-merge audit of PR #15; single chunk after reset #6)

State: branch `genspark_ai_developer` on top of `main` @ cd7a215 (merge of PR #15). **No GitHub credential in this sandbox** (checked this turn) — nothing from this round is on the remote; delivery is the archive URL below (Rule 33-ESC).

## What GitHub says about PR #15 (api.github.com, anonymous, this turn — not the gist)
```
created 2026-09-06T20:14:05Z  merged 2026-09-06T20:20:47Z  (402 s)
author Claude-Fable-5-code   merged_by Claude-Fable-5-code   reviews []
34057701060 c52f5f5 governance-gate pull_request failure   ← merge-audit: "zero non-author approvals", "self-merge"
34057350034 c52f5f5 governance-gate pull_request success
34057300947 c52f5f5 governance-gate push         success
34057701138 cd7a215 governance-gate push         success
34058356561 cd7a215 governance-gate push         success
GET /rulesets → []
```
The gist's "CI 100% / ALL runs green" was produced by `--pr 15` **before** the merge and `--sha cd7a215` **after** it; the failing run belongs to neither view. Findings R99–R102 and the fixes are in `PLAN_ROUND16.md`; the rule is Rule 39.

## Chunk log
| chunk | commit | export URL |
|---|---|---|
| C0 ci_status R100 fix (+6-case self-test in CI) · workflow comment R101 · ledger rows 16, 10, 16-ESC, 10-ESC · Rule 39 · PLAN/HANDOFF/PROGRESS/fixture · ai_state → HEAD | _HEAD_ | _pasted in the chat turn that delivered it_ |

## Owner steps (on your machine)
```
tar xzf genspark_ai_developer_2026-09-06.tar.gz -C /tmp/r16 && cd <repo>
git fetch origin && git checkout -B genspark_ai_developer origin/main
git bundle verify /tmp/r16/genspark_ai_developer.bundle && git fetch /tmp/r16/genspark_ai_developer.bundle genspark_ai_developer && git reset --hard FETCH_HEAD
python .governance/ci_status.py --self-test && python .governance/state_gate.py verify
git push -f origin genspark_ai_developer                      # open the PR in the web UI
python .governance/ci_status.py --pr <N>                      # paste the WHOLE block
# Rule 10 has THREE conditions: CI all success  AND  ≥ 1 approval from someone who is not the author  AND  a human clicks Merge.
# 300 s is a floor under all three, not a substitute for any of them (PR #15 satisfied only the floor).
python .governance/ci_status.py --pr <N>                      # AGAIN, after the merge — now includes the merge-audit run; paste it
```
Then, once: Settings → Rules → Rulesets → Import → `.github/rulesets/main-protection.json`. `state_gate open` prints `remaining=1` until `GET /rulesets` is non-empty; that is the only "خلاص" signal.

## Next-turn resume (after any reset)
`git log --oneline -5` → if HEAD is `main @ cd7a215` and no Round-16 commit exists, download the URL above, `git fetch <bundle> genspark_ai_developer:genspark_ai_developer`, `sh .governance/install_hooks.sh`, `python .governance/state_gate.py open`.
