# HANDOFF — Round 12 (written chunk by chunk; sandbox reset twice this round)

State: branch `genspark_ai_developer` rebuilt from `main` @ 544670d (PR #11 merged + human_msg_round12.txt). Every chunk is a local commit; **push blocked — no GitHub credential survives the reset** (`setup_github_environment` → no token; `git push` → "could not read Username"). Owner or next session pushes; see "Push" below.

## Findings R81-R84 (detail in ROUND12_REVIEW.md)
R81 typed `✅ claim_check:` verdict in prose (gist line 246) over a turn scoring 16 contradictions · R82 PROGRESS.md / ai_state.json "updated" with no remote_proof (Rule 25 repeat) · R83 human said "تتاكد انك فاهم قبل ما تبحث … مش تخمن", agent grepped; no gate mode existed for it · R84 human's core complaint: bugs named from partial reads, nothing proves the file was read.

## Chunks (PLAN_ROUND12.md is the checklist; each row = one commit)
C0 done — PLAN_ROUND12.md
C1 done — intent_gate.py: CONFIRM-FIRST (CONFIRM_TRIGGERS, AMBIGUITY ≥2, verify_confirm ```mirror contract); self-test incl. real r12 message
C2 done — claim_check.py: C7 typed-verdict; self-test incl. gist r12 (2 blocks, 16 contradictions)
C3 done — read_proof.py: index (lines/sha/def-class-section spans) + check (no proof / stale sha / wrong file); self-test
C4 done — attest.py grammar: read_proof + C[1-7]; fixture agent_gist_round12.md fetched raw (541 lines, sha256 eb259fcd1a5ff6cb…)
C5 done — Rules 27-29; FULL_READ Steps 0a/2b/4c; CI "checker family self-tests" step in live workflow AND pending/ (owner applies if `.github/workflows` push is rejected)
C6 done — ROUND12_REVIEW (13 REQ, --full 663/663), anchor agent_hard_rules_r12 (218 lines, sha 11fbb7ec…), 7 skills bumped, this handoff
C7 — squash → push → PR (blocked on credential; commands below)

## Verify (from a clean checkout of the branch)
```
python .governance/intent_gate.py --self-test
python .governance/claim_check.py --self-test
python .governance/read_proof.py --self-test
python .governance/attest.py verify docs/audit_reports/context-connect/context-connect/fixtures/agent_gist_round12.md
python .governance/claim_check.py docs/audit_reports/context-connect/context-connect/fixtures/agent_gist_round12.md      # expect rc=1, 16 hits incl. C7
python .governance/intent_gate.py detect docs/audit_reports/context-connect/context-connect/fixtures/human_msg_round12.txt   # expect CONFIRM-FIRST
python .governance/req_coverage.py docs/audit_reports/context-connect/context-connect/ROUND12_REVIEW.md --source docs/audit_reports/context-connect/context-connect/fixtures/human_msg_round12.txt --full
python .governance/secret_scan.py && python .governance/path_scan.py
```

## Push (whoever has a credential)
```
git fetch origin && git rebase origin/main            # main is 544670d at time of writing
git reset --soft origin/main && git commit -m "feat(governance): Round-12 — CONFIRM-FIRST mirror (R83), read_proof (R84), claim_check C7 (R81), Rules 27-29"
git push -f origin genspark_ai_developer
gh pr create --base main --head genspark_ai_developer --title "Round 12: mirror-before-act, read-proof, typed-verdict guard" --body-file docs/audit_reports/context-connect/context-connect/HANDOFF_ROUND12.md
```
Do NOT self-merge (Rule 10/13). Wait for `gate` + one review.

## For whoever resumes after a reset
`git log --oneline -8` — if the top commit says `[C6]`, only C7 remains. Do not re-do chunks; `PLAN_ROUND12.md` checkboxes are authoritative.
