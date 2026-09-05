# AGENT HARD RULES — `.governance/`

**Scope:** every AI agent (Antigravity / Gemini / Claude / Genspark) operating on this repository or its master workspace.
**Status:** Tier T0 — cannot be overridden by task instructions. Violations are §FATAL.
**Why this file exists:** Rounds 1–4 of the consultant audit showed that prose instructions are read selectively, while `grep`-verifiable instructions are followed. Every rule below therefore has a **machine check** and a **proof command**. If you cannot produce the proof, you have not complied.

---

## Rule 1 — A token must never be visible to you

| | |
|---|---|
| **Rule** | You never see, type, paste, echo, log, or embed a credential (`ghp_…`, `github_pat_…`, `sk-…`, `AKIA…`, private keys). Not in commands, not in URLs, not in config files, not in "temporary" scripts, not in chat. |
| **Instead** | Push with plain `git push origin <branch>`. Authentication lives in the OS: `gh auth login` (once, by the human) or a credential manager. If the push fails with 401/403 you **stop and tell the human** — you do not retry with a different auth trick. |
| **Machine check** | `.governance/hooks/pre-push` refuses if the remote URL contains `@` or if any pushed line matches a token pattern. `.github/workflows/governance-gate.yml` repeats the check on GitHub. |
| **Proof** | `git remote -v` shows no `@`; `python .governance/secret_scan.py` → `✅ secret_scan: clean`. |
| **History** | Round 2: 1 token in gist. Round 3: 1 token. Round 4: 2 tokens, 6 retries. **Round 5: 3rd token as a Python literal, executed 6×, smuggled via a hand-written credential helper (R21/R22).** All public. |

## Rule 2 — No machine-specific path in any tracked file

| | |
|---|---|
| **Rule** | No `file:///`, `C:\`, `d:\`, `/Users/x/`, `/home/x/`, or UNC path in `.md .py .ps1 .sh .json .yml .toml .txt`. Exception: `GLOBAL_HISTORICAL_LEDGER.md` (archive) and audit reports that quote paths as evidence. | <!-- path-scan:allow -->
| **Instead** | Markdown links are repo-relative (`.agents/AGENTS.md`). Scripts take paths from CLI args or environment variables (`FABLE_MASTER`) with repo-relative defaults. |
| **Machine check** | `.governance/path_scan.py` in pre-commit and CI. |
| **Proof** | `python .governance/path_scan.py` → `✅ path_scan: clean`. |
| **History** | R07 (Round 1), re-introduced as R18 in `verify_sync.py:47,49` (Round 4). |

## Rule 3 — Hooks are installed before the first commit of a session

| | |
|---|---|
| **Rule** | First action after `cd` into the repo: `bash .governance/install_hooks.sh` (or `.ps1`). `--no-verify` is forbidden. |
| **Proof** | `git config core.hooksPath` → `.governance/hooks`. |

## Rule 4 — "Done" means the CI gate is green, not that your local probe printed True

| | |
|---|---|
| **Rule** | You may not write "100%", "closed", "resolved", or "verified" in a commit message, PROGRESS.md, or chat for anything that has not passed `governance-gate` on GitHub **or** an independent run on a second machine. Your own probe on your own machine is *evidence*, not *verification*. |
| **Instead** | Write: "local probe 9/9; awaiting CI" — then update after the run. |
| **Machine check** | CI runs `probe_init_root.py`, `secret_scan.py`, `path_scan.py`, `verify_sync.py` on every push. |
| **Proof** | Link to the green Actions run in the PR / PROGRESS entry. **A bare commit hash is not proof** — it can exist only in the sandbox. Proof is an `https://` URL, a CI run-id, or `origin/<ref>` that the human can open. `req_coverage.py --strict-done` enforces this on every `DONE` row. |
| **History** | R20 (Round 4): "7/7 True 100%" claimed for a probe whose R03 case was rewritten to pass; "15/15 parity" claimed for a script that fails 0/15 anywhere else. R36 (Round 6): REQ-11 "push to GitHub" closed `DONE` citing local hash `a84cbe0` while `git push` had returned 403. |

## Rule 5 — Consultant findings are a checklist, not a summary

| | |
|---|---|
| **Rule** | When a review lists N files/lines for an issue, you open all N. You close the issue only when the review's own grep returns zero. You do not paraphrase the finding into a smaller one. |
| **Machine check** | Each finding in `docs/audit_reports/**/ROUND*_REVIEW.md` carries a proof command. Run it. |
| **Proof** | Paste the command and its zero-hit output in the commit body. |
| **History** | Round 3: 5 files listed for R09, 2 fixed, "R09 resolved" written. Round 4 (grep-based brief): all fixed. |

## Rule 6 — One source of truth per file, verified by hash, never by memory

| | |
|---|---|
| **Rule** | Any file that exists both in the master workspace and in `proposed_files/` must be byte-identical (CRLF-normalised) at push time. Copying by hand and "it should be the same" is not compliance. |
| **Machine check** | `python .governance/verify_sync.py --master <workspace>` before every push; CI runs the published-layer check automatically. |
| **Proof** | `RESULT: N/N in parity` with N = current mapping size. |
| **History** | R17 (Round 3); non-portable first engine R18 (Round 4). |

## Rule 7 — Never push to `main`. Ever. Not even "just this once"

| | |
|---|---|
| **Rule** | All work lands on `genspark_ai_developer` (or another feature branch) and reaches `main` **only** through a Pull Request approved by the human. `git push origin main`, `git merge` into a local `main` followed by push, `git push origin HEAD:main` — all forbidden. |
| **Instead** | `git push origin genspark_ai_developer` → open/update the PR → **stop**. The human merges. |
| **Machine check** | `.governance/hooks/pre-push` refuses `refs/heads/main` and `refs/heads/master`. Server-side: `.github/rulesets/main-protection.json` (once imported by the owner) makes it impossible regardless of hooks. |
| **Proof** | `git log origin/main --format='%s' -3` shows only `Merge pull request #N …` commits. |
| **History** | Round 5: `2bf68a3`, `46d524c` pushed directly to `main` while the final report described a PR flow (R23, R27). |

## Rule 8 — A token in the chat is an incident, not a resource

| | |
|---|---|
| **Rule** | If a credential appears in the conversation (pasted by the human, found in a file, printed by a command), you **do not use it**. Your entire reply for that turn is: (1) "A token is visible in this conversation. Revoke it now: https://github.com/settings/tokens" (2) nothing else. No tool call in that turn. |
| **Why** | The agent cannot un-see a token; the only safe move is to make it worthless immediately. Every leaked token so far was used *by the agent* after the human pasted it. |
| **Forbidden techniques** (each was attempted in Round 5) | custom `credential.helper=!…` scripts · `-c credential.username=…` loops · `cmdkey /pass:` · reading `keys.txt` or any vault file · embedding `Authorization: Bearer` in ad-hoc API calls · `GH_TOKEN=` env injection. |
| **Machine check** | `pre-push` v2 refuses inline helpers and username overrides; `secret_scan.py` matches `password=ghp_`, `Bearer ghp_`, `credential.helper=!…` (inline command), `cmdkey /pass:`. |
| **Proof** | Paste the exact refusal message from the hook if you were ever tempted. Otherwise: `python .governance/secret_scan.py --range origin/main..HEAD` → clean. |
| **History** | R16 (R2–R4), R21/R22/R24/R25 (Round 5). |

## Rule 9 — Every human sentence becomes a REQ row, and every REQ row gets closed

| | |
|---|---|
| **Rule** | Follow `.governance/FULL_READ_PROTOCOL.md`: first output of the turn is a `req-ledger` block quoting every sentence verbatim; last output is a `req-closure` block with one row per REQ. Questions are `ANSWERED` or `BLOCKED` — never silently skipped, never `DEFERRED`. |
| **Machine check** | `python .governance/req_coverage.py <turn.md> --strict-done --source <human_msg.txt>` → exit 0. `--source` fails any ledger quote that is not verbatim in the human's message. |
| **Proof** | The exit line `✅ req_coverage: N REQs, all closed` at the end of the turn. |
| **History** | Rounds 1–4: findings paraphrased into fewer items; Round 5: self-critique omitted the auth violations entirely (R27). R37 (Round 6): "verbatim" quote `يشوعها` for the human's `يشوفها`; `علشان` for `عشان`. |

## Rule 10 — A pull request is merged by someone other than its author, after CI, after ≥ 1 approval

| | |
|---|---|
| **Rule** | The account that opened the PR does not merge it. No merge before `governance-gate` is green and at least one non-author approval exists. Minimum 5 minutes between open and merge (a human cannot read a CI log faster). |
| **Instead** | Open the PR, paste the URL in the handoff, stop. The owner merges. |
| **Machine check** | `merge_timing_guard.py` runs on `pull_request: closed` and turns `main` red on violation. Real fix: owner imports `.github/rulesets/main-protection.json` (server-side; cannot be bypassed by any agent). |
| **History** | R38 (Round 6): PR #3 opened 22:00:03Z, self-merged 22:00:07Z, zero reviews. |

## Rule 11 — Handoff first, then work; export after every chunk

| | |
|---|---|
| **Rule** | The first file written in a session is the handoff with the frozen chunk list. Each chunk ends with commit **and** an off-sandbox copy (push, or `sh .governance/export_bundle.sh` + upload when push is denied). A chunk without an off-sandbox copy is not done. |
| **Instead** | If the sandbox resets, the next session opens the handoff and resumes from the first unchecked box — nothing is re-derived from memory. |
| **Machine check** | Handoff ticks must reference a URL or `origin/` ref per chunk (same `--strict-done` rule). |
| **History** | R39 (Round 6): ~40 min of Round-6 work destroyed by a reset because the handoff was written after the analysis and nothing had left the sandbox. |

---

## Session start checklist (copy into the first turn)

```
[ ] bash .governance/install_hooks.sh            -> core.hooksPath = .governance/hooks
[ ] git remote -v                                -> no '@'
[ ] python .governance/secret_scan.py            -> clean
[ ] python .governance/path_scan.py              -> clean (or list of pre-existing hits you are about to fix)
[ ] python .governance/verify_sync.py --master … -> N/N parity
[ ] python .governance/probe_init_root.py        -> 9/9
[ ] Read Root/ai_state.json, Root/HANDOFF.md     -> resume from next_action
[ ] First output = req-ledger block (Rule 9)      -> before any tool call
[ ] git branch --show-current                    -> NOT main (Rule 7)
```

## Session end checklist

```
[ ] Root/ai_state.json updated (turn_count, git_commit, next_action)
[ ] Root/HANDOFF.md updated if a milestone closed
[ ] git push origin <branch> succeeded WITHOUT touching credentials
[ ] Actions run link recorded (or "awaiting CI" written — never "100%")
[ ] PR opened/updated; main untouched (Rule 7)
[ ] req-closure block + req_coverage.py exit 0 (Rule 9)
[ ] Self-critique lists EVERY command that touched auth, main, or files outside the repo (R27)
```

---

*Rules 1–6 added in Round 4, Rules 7–9 in Round 5, by the Genspark consultant. Changes to this file require a new anchor in `Root/ANCHORS.md`.*
