# HANDOFF — Round 14 (two sandbox resets; C0–C4 came back from their own export)

State: branch `genspark_ai_developer` rebuilt on top of `main` @ 463a967 (the guide commit). **No GitHub credential in this sandbox** (`setup_github_environment` → "No Valid GitHub Authorization Found", checked after reset #1 and reset #2). `git push` was attempted once after reset #2 and failed on "could not read Username" — nothing is on the remote from this round. `origin/genspark_ai_developer` = 848b62b is **stale** (Round-13 guide on top of 1a8d59d, not an ancestor of main) → push with `-f`.

## Findings R90–R94 → Rules 35–37 (detail + req ledger in ROUND14_REVIEW.md, forensic detail in ROUND14_PREFLIGHT_AUDIT.md)
R90 state file promised, never read → `state_gate.py` · R91 same rule broken twice, unnoticed → `mistakes.py recurrence` + `<n>-ESC` rows · R92 `edit_proof before/after --scope` did not exist → `edit_proof.py show --scope A-B` on real hunks · R93 no placeholder checker → `mock_scan.py` in pre-commit + CI · R94 guide described an auto-merge script and wrong commands → guide rewritten.

## Chunk log (SHAs are the local branch SHAs; URL = the off-sandbox copy; each archive contains all earlier chunks)
| chunk | commit | export URL |
|---|---|---|
| C0 plan + fixture + preflight audit | d59ad56 | https://www.genspark.ai/api/files/s/AfBDOpPW |
| C1 state_gate.py + grammar | 214ad46 | https://www.genspark.ai/api/files/s/mq5nSG4O |
| C2 precheck step 0, self_review Q7, PROGRESS.md, ai_state healed | 6f7d17c | (URL lost in reset #2; inside every later archive) |
| C3 pre-commit "state moves with code" + CI state gate | 1af78d7 | (same) |
| C4 mistakes.py recurrence + 33-ESC row | 1a644ea | https://www.genspark.ai/api/files/s/ML4i1Ygy |
| — reset #2 — recovered C0–C4 from the C4 archive, SHAs identical | | |
| C5a edit_proof --scope + grammar + CI R92 | d44a583 | https://www.genspark.ai/api/files/s/9d29NdGQ |
| C5b mock_scan.py + hook + grammar + CI R93 | 75463b2 | https://www.genspark.ai/api/files/s/kaEAS4ip |
| C6a USER_COMPLETE_OPERATING_GUIDE.md corrected | ba74cc2 | https://www.genspark.ai/api/files/s/y4X9hU7M |
| C6b Rules 35–37, protocol steps, 7 skills, plan ticks | f4a6361 | https://www.genspark.ai/api/files/s/SqJJGyeF |
| C6c this handoff + ROUND14_REVIEW.md (--full 555/555) | 124dc83 | https://www.genspark.ai/api/files/s/8q8Vr7DK |
| C7 squash → one commit (tree identical to C6c except ai_state.json) | 3e839a1 | https://www.genspark.ai/api/files/s/mc7zSGK9 |
| C7+ URL row (**apply THIS archive: 2 commits = squash + this row**) | _HEAD_ | _pasted in the chat turn that delivered it_ |

## Owner steps (on your machine; token goes into the credential manager, never into chat)
```bash
# 1. take the LATEST archive URL from PLAN_ROUND14.md (C7 row once ticked, else the highest chunk)
tar xzf r14_*.tar.gz -C /tmp/r14
cd <repo> && git fetch origin && git checkout -B genspark_ai_developer origin/main
git am /tmp/r14/0*.patch            # or: git fetch /tmp/r14/genspark_ai_developer.bundle genspark_ai_developer:genspark_ai_developer
bash .governance/install_hooks.sh   # core.hooksPath=.governance/hooks (pre-commit now runs mock_scan + state_gate verify)
for s in state_gate mistakes edit_proof mock_scan precheck self_review; do python .governance/$s.py --self-test; done
python .governance/state_gate.py verify && python .governance/mistakes.py recurrence
git push -f origin genspark_ai_developer
# 2. open the PR genspark_ai_developer → main; wait for the governance-gate workflow (new steps: state gate, R91/R92/R93 negatives, hook stub negative)
python .governance/ci_status.py --pr <N>
# 3. merge MANUALLY after CI green + the 300 s merge_timing_guard floor + your review. No script merges for you (R94, Rules 10/13/20).
```

## After merge, the next session starts with
```bash
python .governance/attest.py run -- python .governance/state_gate.py open      # first block of the turn (Rule 35)
cat .governance/MISTAKES.md                                                     # rows + ESC rows (Rule 36)
```

## Known limits (stated so nobody over-trusts this round)
- CI has not run on this branch. Every negative in the new workflow steps was replicated in the sandbox, not on GitHub Actions.
- `edit_proof --scope` measures against HEAD; commit between two scoped edits to the same file.
- `mock_scan` P6 (constant-return stub) is a heuristic (work-verb name + single-line body). P1–P5 are exact matches.
- `state_gate` cannot force the agent to *call* it; `precheck.py` step 0 and the pre-commit hook make a turn or commit without it fail — the human still has to run/see precheck.
- Two export URLs (C2, C3) were lost with reset #2; their content is in every later archive and in the C7 squash.
