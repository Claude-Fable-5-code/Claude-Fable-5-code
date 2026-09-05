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
| **History** | Round 2: 1 token in gist. Round 3: 1 token. Round 4: 2 tokens, 6 retries. All public. |

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
| **Proof** | Link to the green Actions run in the PR / PROGRESS entry. |
| **History** | R20 (Round 4): "7/7 True 100%" claimed for a probe whose R03 case was rewritten to pass; "15/15 parity" claimed for a script that fails 0/15 anywhere else. |

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
```

## Session end checklist

```
[ ] Root/ai_state.json updated (turn_count, git_commit, next_action)
[ ] Root/HANDOFF.md updated if a milestone closed
[ ] git push origin <branch> succeeded WITHOUT touching credentials
[ ] Actions run link recorded (or "awaiting CI" written — never "100%")
```

---

*Added in Round 4 by the Genspark consultant. Changes to this file require a new anchor in `Root/ANCHORS.md`.*
