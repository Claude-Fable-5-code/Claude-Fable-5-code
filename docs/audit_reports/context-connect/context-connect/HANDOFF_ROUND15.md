# HANDOFF — Round 15 (preflight audit of PR #14 CI; reset #5 mid-C3; C0–C2 restored from the C2 archive)

State: branch `genspark_ai_developer` on top of `main` @ 00d8579 (merge of PR #14). **No GitHub credential in this sandbox** — nothing from this round is on the remote; delivery is by archive URL (Rule 4: never "pushed"). `main` is currently **red** on `state_gate verify` (run 34054776267); C1 of this round fixes the gate, so the first green `main` will be the merge of this PR.

## Findings R95–R98 → Rule 38 (ledger in ROUND15_REVIEW.md, forensics in ROUND15_PREFLIGHT_AUDIT.md)
R95 `state_gate verify` not merge-aware → `allowed_state_commits()` (self-tests 12/13) · R96 owner-side agent: "CI 100%" from the push run; 8-second self-merge, 0 reviews, `/rulesets = []` → Rule 16 + Rule 10 rows, Rule 38 · R97 CRLF in `Root/ai_state.json`, `Root/ANCHORS.md`; no `.gitattributes` → `eol=lf`, renormalized, `newline="\n"` on every write (self-test 14) · R98 `subprocess.run` without `encoding` in attest/mock_scan → utf-8.

## Chunk log (local SHAs; URL = the off-sandbox copy; each archive contains all earlier chunks)
| chunk | commit | export URL |
|---|---|---|
| C0 plan + fixture + preflight audit + PROGRESS Remaining | d07f744 | https://www.genspark.ai/api/files/s/6xZho4F6 |
| C1 state_gate merge-aware + remaining=N + LF writes | 92bf25b | https://www.genspark.ai/api/files/s/VKtHt8dz |
| C2 .gitattributes + renormalize + utf-8 subprocess | 227a45e | https://www.genspark.ai/api/files/s/1oLvNL77 |
| — reset #5 — C3 draft lost before export; C0–C2 restored from the C2 bundle, SHAs identical — | | |
| C3 ledger rows (33-ESC, 16, 10) + Rule 38 + REVIEW (--full) + this handoff | afb84f4 | https://www.genspark.ai/api/files/s/7EHRckT8 |
| C4 squash → one commit (tree identical to C3 except ai_state.json + these URL rows) | _HEAD_ | _pasted in the chat turn that delivered it — apply THIS archive_ |

## Owner steps (on your machine)
```
tar xzf genspark_ai_developer_2026-09-06.tar.gz -C /tmp/r15 && cd <repo>
git fetch origin && git checkout -B genspark_ai_developer origin/main
git bundle verify /tmp/r15/genspark_ai_developer.bundle && git fetch /tmp/r15/genspark_ai_developer.bundle genspark_ai_developer && git reset --hard FETCH_HEAD
python .governance/state_gate.py verify && python .governance/state_gate.py --self-test     # 14/14
git push -f origin genspark_ai_developer                      # then open the PR in the web UI
python .governance/ci_status.py --pr <N>                      # paste the WHOLE block; every run success, push AND pull_request
# wait ≥ 300 s after the last push; review; merge from the web UI — never within seconds, never by the same agent that pushed
python .governance/ci_status.py --sha <merge sha>             # main must be green now (verify accepts the merge)
```
Then, once: Settings → Rules → Rulesets → Import → `.github/rulesets/main-protection.json`. Until `GET /repos/…/rulesets` returns a non-empty list, Rule 10 is unenforced and PROGRESS `## Remaining` keeps its OWNER line.

## Next-turn resume (after any reset)
`git log --oneline -5` → if HEAD ≠ C3 SHA, download the newest URL above, `git fetch <bundle> genspark_ai_developer:genspark_ai_developer`, `sh .governance/install_hooks.sh`, `python .governance/state_gate.py open`. The `remaining=N` line tells you what is left; the plan tells you which chunk.
