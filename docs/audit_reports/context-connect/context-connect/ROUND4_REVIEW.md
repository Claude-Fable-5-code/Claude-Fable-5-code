# Round 4 — Independent Review of `f9d7d02`

**Reviewer:** Genspark consultant (independent, read-only against `origin/main`)
**Target commit:** `f9d7d02` (12 files, +163/−44)
**Prior baseline:** `7377ad7`
**Method:** every claim below was re-executed on Linux in an isolated worktree. Nothing is taken from the agent's own probe output.

---

## 1. Verdict in one line

Real progress (R07/R09/R03/R14 are genuinely closed), **but** the commit introduced one new regression (`verify_sync.py` is not runnable anywhere except the agent's own machine) and the agent leaked a **fourth** GitHub token into a public gist.

---

## 2. Claim-by-claim

| # | Agent claim | Independent result | Status |
|---|---|---|---|
| 1 | `grep file:///` → 0 hits in `proposed_files/` | 0 hits outside `GLOBAL_HISTORICAL_LEDGER.md` (1 hit is a *description of the bug* inside `PROGRESS.md:136`, acceptable) | ✅ **R07 closed for `.md` files** |
| 2 | Old sync wording → 0 hits | 0 hits for `بعد كل خطوة|اللحظي|وخطوة|مع كل تعديل`. Only word left is the title «القهرية» which is a label, not an instruction | ✅ **R09 closed** |
| 3 | R03 rerun preserves full state | Custom key `marker=KEEP` now survives as a **real key** (not stuffed into a string). `turn_count=42` kept. 9 keys after rerun = 8 contract + 1 user | ✅ **R03 closed** (design changed from strict-contract to preserve-all; acceptable) |
| 4 | Traversal / absolute paths blocked | `../x` rc≠0, `/tmp/x` rc≠0 | ✅ still holds |
| 5 | Anchors 10/10 | 10/10 SHA-256 match, 0 duplicates | ✅ |
| 6 | `PROGRESS.md` updated (R14) | P14 entry present and describes `7377ad7` accurately | ✅ **R14 closed** |
| 7 | `verify_sync.py` 15/15 parity — "run before every push" | **Fails 0/15 on any machine that is not the agent's.** Lines 47 & 49 hard-code `C:\Users\pc\.gemini\...` and `d:\SMS\.hRhRhRhRhRhR`. The very file meant to close R17 re-opens R07. | ❌ **R17 NOT closed — regression** |
| 8 | Remote URL clean (R16) | `git remote -v` clean — true. But the gist shows token `ghp_7XO6…` used in ≥6 commands, then a **new** token `ghp_Llu676…` pasted into `git remote set-url`. Both in a public gist. | ❌ **R16 escalated** |
| 9 | Commit message "R17 verify_sync engine" | Engine exists but is non-portable and untested outside author machine | ⚠️ misleading |

Score: **6 ✅ / 2 ❌ / 1 ⚠️**

---

## 3. What actually went wrong this round (root causes, not symptoms)

### 3.1 Token leakage is a *process* failure, not a one-off
Timeline in the gist:
1. Writes token into `.git/credentials` → push fails (`Invalid username or token`).
2. Writes token into `~/.git-credentials` → fails.
3. `git remote set-url` with token → fails.
4. `git push https://TOKEN@github…` inline → fails.
5. Deletes `.git-credentials`, tries `ls-remote` with token → fails.
6. User supplies **new** token → agent pastes it inline into `set-url` → push succeeds.

Six retries, two tokens, all visible in a public gist. The agent's closing line "Revoke ghp_Llu…" is correct advice but it is the agent who exposed it. **Any workflow where the agent can see the token will leak it.** The fix is architectural (§5.1).

### 3.2 `verify_sync.py` — solving the right problem the wrong way
The parity idea (R17) is correct. Implementation is wrong because the agent tested it only where it was written. It also **maps `proposed_files/README.md` → `README.md` of the master**, so it silently accepts that the published repo's own `README.md` differs from `proposed_files/README.md` — which is exactly the drift R17 was supposed to catch.

### 3.3 Selective reading persists
The Round-3 report listed 3 leftover files for R09 and 3 for R07 with line numbers. This round the agent used `grep` (as instructed) and caught them all — **grep-driven instructions work, prose-driven instructions don't.** Keep that in mind when writing the next brief.

---

## 4. Register after `f9d7d02`

| ID | Title | Round 3 | Round 4 |
|---|---|---|---|
| R01 | Secrets in templates / `.gitignore` | CLOSED | CLOSED |
| R02 | `init_root.py` path traversal | CLOSED | CLOSED |
| R03 | `init_root.py` rerun overwrite | CLOSED (with note) | **CLOSED** (note resolved) |
| R04 | `init_root.py` validation / exit code | CLOSED | CLOSED |
| R05 | `ai_state.json` key contract + HANDOFF | CLOSED | CLOSED |
| R07 | Absolute Windows paths | PARTIAL | **PARTIAL** — `.md` clean; `verify_sync.py:47,49` hard-coded |
| R09 | Lean Sync wording | PARTIAL | **CLOSED** |
| R11 | `.gitignore` remote | CLOSED | CLOSED |
| R12 | Anchor duplicates | CLOSED | CLOSED |
| R14 | `PROGRESS.md` stale | OPEN | **CLOSED** |
| R15 | `.gitignore` over-broad | CLOSED | CLOSED |
| R16 | Token in command line | OPEN P0 | **OPEN P0 — 2 more tokens exposed** |
| R17 | Master ↔ `proposed_files` parity gate | OPEN P2 | **OPEN P1** — engine non-portable |
| **R18** | `verify_sync.py` hard-codes `C:\Users\pc\…` and `d:\SMS\…` | — | **NEW P1** |
| **R19** | No automated secret scan on push/PR | — | **NEW P0** (root cause of R16 recurring) |
| **R20** | Agent self-reports "100%" before independent run | — | **NEW P2** (behavioural) |

Open: **R07, R16, R17, R18, R19, R20** — of which R16+R19 are the same disease.

---

## 5. Prevention — what is delivered in this PR

Everything below is a file, not a suggestion. All live under `/.governance/` so they can be copied into the master workspace as one folder.

| File | Purpose | Closes |
|---|---|---|
| `.governance/hooks/pre-push` | Blocks any push whose diff contains a token-shaped string (`ghp_`, `github_pat_`, `sk-`, `AKIA…`, `xox…`, private-key headers). Also blocks if remote URL contains `@`. | R16, R19 |
| `.governance/hooks/pre-commit` | Same scan on staged files, plus rejects `file:///`, `C:\`, `d:\` in `.md`/`.py` (except `GLOBAL_HISTORICAL_LEDGER.md`). | R07, R18, R19 |
| `.governance/install_hooks.sh` / `.ps1` | One-shot installer (`core.hooksPath`). | — |
| `.governance/secret_scan.py` | Portable scanner used by both hooks and CI. Exit 1 on hit. | R19 |
| `.governance/path_scan.py` | Portable absolute-path scanner. Exit 1 on hit. | R07, R18 |
| `.governance/verify_sync.py` | Portable replacement for root `verify_sync.py`: takes `--master` and `--proposed` as args or env (`FABLE_MASTER`, `FABLE_PROPOSED`), defaults to repo-relative, never hard-codes. Also checks **published** files vs `proposed_files/` (the drift R17 was meant to catch). | R17, R18 |
| `.github/workflows/governance-gate.yml` | Runs the three scanners on every push/PR to `main`. A leaked token or absolute path **fails CI** even if hooks were bypassed. | R16, R19, R07 |
| `.governance/AGENT_HARD_RULES.md` | Six rules the agent must load before any git operation — written as **grep-verifiable** statements, because §3.3 shows that is the only form the agent follows. | R16, R20 |

Root `verify_sync.py` is **not deleted** in this PR (the agent's PROGRESS/ANCHORS reference it). It should be replaced by `.governance/verify_sync.py` in the agent's next commit; the pre-commit hook will flag its hard-coded paths until then.

---

## 6. Actions for the human (cannot be automated)

1. **Revoke** `ghp_7XO63LUK…` and `ghp_Llu676dV…` at <https://github.com/settings/tokens>. Both are in a public gist.
2. **Never paste a token into the chat.** Instead: `gh auth login` once on the machine, or set `GH_TOKEN` in the OS environment outside the agent's view. The agent should only ever run `git push origin main` and see success/failure.
3. Delete or make private the three gists that contain tokens.
4. Enable **GitHub Secret Scanning + Push Protection** on the repo (Settings → Code security). It is free for public repos and would have blocked pushes 1-5 in §3.1.

---

## 7. Brief for the agent (copy verbatim)

```
Round 4 verified. R03/R09/R14 closed. Two failures:

1. R18: verify_sync.py lines 47,49 hard-code C:\Users\pc and d:\SMS. Delete root verify_sync.py,
   use .governance/verify_sync.py --master <path> --proposed proposed_files. Proof:
   `python .governance/path_scan.py` → exit 0.

2. R16/R19: two tokens leaked (ghp_7XO6…, ghp_Llu6…). Rules now in .governance/AGENT_HARD_RULES.md.
   Run `bash .governance/install_hooks.sh` (or .ps1). Proof:
   `git config core.hooksPath` → .governance/hooks ; `git remote -v` contains no "@".

3. Copy .governance/ into master workspace d:\SMS\.hRhRhRhRhRhR\.governance\ and add it to verify_sync mapping.

Do not report "100%" for anything you did not run on a second machine or in CI.
The CI workflow .github/workflows/governance-gate.yml is the second machine.
```
