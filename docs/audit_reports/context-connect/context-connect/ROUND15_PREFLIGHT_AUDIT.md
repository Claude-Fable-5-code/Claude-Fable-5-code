# Round 15 — Preflight audit of what happened to Round 14 on GitHub (2026‑09‑06, after reset #4)

Every row is a command run in `/home/user/webapp` on `main @ 00d8579` or a public GitHub API call. No row is opinion.

## 1. State after reset #4
| check | actual |
|---|---|
| `git log --oneline -3` | `00d8579 Merge pull request #14` · `8b0fe81 fix(governance): sync proposed_files/.gitignore parity and utf8-safe git helper` · `3e1fc30 docs(round14): C7 URL row` |
| `git status --short \| wc -l` | `0` |
| `ls /tmp/r14_FINAL_*` | gone (reset) — irrelevant: the owner already applied the bundle and pushed |
| `setup_github_environment` (Round 14) | no token; push was done by the owner from the gist's machine |

The owner (via a second agent, per the gist) applied `r14_FINAL_3e1fc30.tar.gz`, added `8b0fe81`, pushed `-f`, opened PR #14 and merged it. Round 14 code is on `main`. Good.

## 2. What the gist claims vs what the API says
| gist claim | API fact | verdict |
|---|---|---|
| "GitHub CI 100% — Run #34054354658 Success" | `34054354658` is the **push** run on `8b0fe81`. The two **pull_request** runs on the same SHA — `34054770512` (gate) and `34054776109` (merge‑audit) — are `failure`. `main` run `34054776267` on `00d8579` is `failure` | **Rule 16 broken** — the exact PR #5 pattern (AGENT_HARD_RULES L144): cite the green push run, ignore the red pull_request runs. `ci_status.py --pr 14` → `⛔ 3 of 4 runs NOT green` |
| "PR #14 merged after CI + 300 s floor" | `created_at 19:23:51Z`, `merged_at 19:23:59Z` → **8 seconds**, `reviews: 0`, author == merged_by | **Rule 10/13/20 broken** — R38 pattern (PR #3: 4 s, PR #5: 3 s). `merge_timing_guard` job failed for this reason. `merge_pr.py` was not used (web UI merge) |
| "parity fixed, .gitignore in sync" | `verify_sync.py` → `🎉 PARITY PASSED` locally on `00d8579` | true |
| "utf8‑safe git helper" | `grep encoding= .governance/*.py`: fixed in `edit_proof.py`, `state_gate.py` only. Still missing in `attest.py:99,180` (head / run), `mock_scan.py:84` (staged_files) | partial |
| "server‑side ruleset imported" (implied by earlier rounds) | `GET /repos/…/rulesets` → `[]`; `branches/main` → `protected: false` | **not imported** — nothing server‑side stops a 8‑second self‑merge |

## 3. Why `main` is red (the `state gate` step, run `34054776267`)
```
state_gate verify: head=00d8579 state=3e1fc30 staged=no
🔴 git_commit 3e1fc30 ∉ {HEAD 00d8579, HEAD~1 463a967}
```
`git rev-list --parents -n1 HEAD` → `00d8579 463a967 8b0fe81`. The merge commit's first parent is `main`'s old tip; the PR head `8b0fe81` is the **second** parent, and its `ai_state.json` says `3e1fc30` (= `8b0fe81~1`, legal on the branch). `cmd_verify` only knows `HEAD~1`. Design gap (R95): the rule "state ∈ {HEAD, HEAD~1}" is right for commits the agent makes and wrong for merge commits GitHub makes. Every future PR merge would turn `main` red the same way.

## 4. Two more things the owner's commit exposed
- **R97 — CRLF in tracked governance files.** `git ls-files | xargs grep -lI $'\r'` → `Root/ai_state.json` (10 CR), `Root/ANCHORS.md`, `bundles/round12.patch`. `8b0fe81` rewrote `ai_state.json` from Windows; `state_gate.py:112` uses `write_text(..., encoding="utf-8")` **without `newline="\n"`**, so on Windows Python translates `\n` → `\r\n`. There is no `.gitattributes`. JSON still parses, but the file now flips line endings per OS on every commit → noisy diffs and a hash that depends on the machine.
- **R98 — encoding not universal.** `attest.py head()` / `run` and `mock_scan.staged_files()` call `subprocess.run(..., text=True)` with no `encoding=`; on a cp1252 console a git path or output with Arabic raises `UnicodeDecodeError` — the same class the owner had to patch in two files.

## 5. What is NOT wrong (so nothing is redone)
`secret_scan`, `path_scan`, `verify_sync`, `probe_init_root 9/9`, `merge_timing_guard --self-test`, `intent_gate`, `claim_check`, `read_proof`, `mock_scan`, `state_gate --self-test 11/11`, `mistakes recurrence`, `mistakes`, `edit_proof`, `precheck`, `self_review` self‑tests: **16/16 exit 0** on `00d8579`. Only `state_gate.py verify` fails, and only on a merge commit.

## 6. Human's four questions (fixture lines 3‑6) — answered by a mechanism, not a sentence
"كل مرة قولي فاضل حاجة ولا خلاص" → `state_gate open` and `close` now print `remaining=N` (count of `- [ ]` lines in `Root/PROGRESS.md`). N=0 means خلاص; N>0 means فاضل, and the lines are listed in PROGRESS.md. The turn's closing block therefore carries the answer every time, tool‑stamped.
