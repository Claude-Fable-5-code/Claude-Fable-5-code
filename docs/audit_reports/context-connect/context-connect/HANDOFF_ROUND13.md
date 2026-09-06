# HANDOFF — Round 13 (three sandbox resets; every surviving chunk exists because it was exported)

State: branch `genspark_ai_developer` on top of `main` @ 1fffe4d (PR #12 merged). **No GitHub credential in this sandbox** (`setup_github_environment` → "No Valid GitHub Authorization Found", checked after each reset); `git push` never attempted (Rule 33). Owner applies the **latest** archive and pushes.

Resets this round: #1 wiped ~40 min / 7 commits with zero exports (R89, MISTAKES row 1). #2 during the rebuild. #3 wiped the monolithic C6 mid-commit (MISTAKES row 3); C0‑C5 were restored from the C5 archive and C6 was redone as C6a/b/c with commit+export in one shell command.

## Findings R85‑R89 (RECONSTRUCTED; detail + req ledger in ROUND13_REVIEW.md)
R85 admissions in prose → `mistakes.py` · R86 "edited X" no diff → `edit_proof.py` · R87 all‑✅ self‑critique → `self_review.py` · R88 checkers run after sending → `precheck.py` · R89 chunks never left sandbox → Rule 33 export‑per‑chunk.

## Chunk log (SHAs are the post‑reset‑#3 `git am` SHAs; URL = the off‑sandbox copy)
| chunk | commit | export URL |
|---|---|---|
| C0 plan + handoff stub + fixture | 3420ad0 | https://www.genspark.ai/api/files/s/TFDXSmP2 |
| C1 mistakes.py + MISTAKES.md + grammar | f52a8cd | https://www.genspark.ai/api/files/s/VBYtS8CC |
| C2 edit_proof.py + grammar | 0a28219 | https://www.genspark.ai/api/files/s/FlMZAtbq |
| C3 self_review.py + grammar | 1d0cc92 | https://www.genspark.ai/api/files/s/YqAQ2Nok |
| C4 precheck.py + grammar | 188fb11 | https://www.genspark.ai/api/files/s/J3kbyjWl |
| C5 Rules 30‑34, FULL_READ steps, CI step | 51ac939 | https://www.genspark.ai/api/files/s/RCPmtSy9 |
| C6a 7 skills bumped + MISTAKES row 3 | 8a80079 | https://www.genspark.ai/api/files/s/g8b2WxWf |
| C6b ROUND13_REVIEW.md (--full 134/134) | 774a2a0 | https://www.genspark.ai/api/files/s/amWgTVpW |
| C6c this handoff | _see PLAN_ROUND13 C6c row_ | _see PLAN_ROUND13 C6c row_ |
| C7 squash + final export | _pending_ | _pending_ |

Each archive = `git bundle` of `origin/main..HEAD` + `format-patch` files. The latest archive contains everything before it.

## Verify (clean checkout of the branch)
```
for s in mistakes edit_proof self_review precheck intent_gate claim_check read_proof; do python .governance/$s.py --self-test; done
python .governance/req_coverage.py docs/audit_reports/context-connect/context-connect/ROUND13_REVIEW.md --source docs/audit_reports/context-connect/context-connect/fixtures/human_msg_round13.txt --full --strict-done
python .governance/secret_scan.py && python .governance/path_scan.py
grep -c "Round 13" .agents/skills/*/SKILL.md      # 7 × 1
```

## Apply + push (whoever has a credential)
```
mkdir r13 && tar xzf r13_C7_<sha>.tar.gz -C r13          # or the latest C6c archive
git fetch origin && git checkout -B genspark_ai_developer origin/main
git am r13/0*.patch
git push -f origin genspark_ai_developer
gh pr create --base main --head genspark_ai_developer --title "Round 13: mistakes ledger, edit-proof, self-review, precheck, export-per-chunk (Rules 30-34)" --body-file docs/audit_reports/context-connect/context-connect/HANDOFF_ROUND13.md
```
Do NOT self‑merge (Rules 10/13). Wait for `gate` + one review. If the push rejects the workflow change, apply `.governance/pending/governance-gate.yml` by hand.

## For whoever resumes after the next reset
1. `git log --oneline -3` on `genspark_ai_developer`; if the branch is gone, download the latest URL above and `git am`.
2. `PLAN_ROUND13.md` ticks + URLs are authoritative; a tick without a URL is not done.
3. Read `.governance/MISTAKES.md` first (Rule 30). Commit and `export_bundle.sh` in the **same** command, always.
