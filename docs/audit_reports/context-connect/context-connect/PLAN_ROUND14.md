# Round 14 — Frozen plan (written FIRST, before any tool work — Rule 11)

Source of truth for this round. After a sandbox reset: open this file, run `git log --oneline -8`,
resume from the first chunk without ✅. Never rebuild from memory.

## Reset log
- Reset #2 (2026‑09‑06, during C5): local branch gone; `origin/genspark_ai_developer` still 848b62b. Recovered by
  downloading the C4 archive, `git bundle verify` + `git fetch <bundle>` → C0‑C4 back with identical SHAs (d59ad56…1a644ea).
  `setup_github_environment` → still no token. Lesson already on the ledger (33‑ESC): export in the same command as the commit.
- Reset #1 (2026‑09‑06, before this file): the Round‑14 preflight audit turn was delivered to the human
  (it survives in the human's gist `16d1dc7b…/9.txt`, sha256 `b3f12a0d…`); nothing was committed. Fresh
  clone of `main` @ `463a967`. `setup_github_environment` → "No Valid GitHub Authorization Found".
  `origin/genspark_ai_developer` = `848b62b` (stale: same guide on top of 1a8d59d, NOT an ancestor of main)
  → this round re‑bases the branch on `main` and the owner pushes with `-f`.

## Human decisions captured (fixture `fixtures/human_msg_round14.txt`)
1. Plan approved verbatim ("تمام وموافق 100%").
2. `state_gate close --write` **must** rewrite `Root/ai_state.json` (HEAD, utc, next_action) itself;
   verification/refusal (exit 1) stays when the update is incomplete or the gate was not called at
   the start AND the end of the turn.
3. C0 = fixture + this plan + `ROUND14_PREFLIGHT_AUDIT.md` + export, in one command.

## Off‑sandbox rule (push substitute — Rule 33)
Each chunk = `git commit` → `sh .governance/export_bundle.sh` → upload → paste URL in the row below,
**in the same shell command as the commit**. A chunk without a URL is NOT done.

## Findings (from the preflight audit, all tool‑verified; detail in ROUND14_PREFLIGHT_AUDIT.md)
- **R90** — Guide §9 claims a compulsory self‑recall at turn start/end. `grep ai_state .governance/*.py`
  → only a regex in claim_check C5 + probe_init_root + remote_proof. No hook, no precheck step, no CI
  step reads or requires the state file. `ai_state.json` is 10 commits behind HEAD (`e9d0bbe` vs `463a967`).
  `Root/PROGRESS.md` does not exist.
- **R91** — `MISTAKES.md` records admissions but nothing detects the *same* rule breaking twice
  (rows 2 and 3 are both Rule 33). Recurrence is invisible.
- **R92** — Guide §3 documents `edit_proof.py before/after --scope A-B`. Those sub‑commands do not exist;
  the tool has `show`/`check` and reads `git diff --numstat` only — it cannot detect an edit outside a line range.
- **R93** — Guide §4 forbids TODO/mock/placeholder code; no checker exists for it.
- **R94** — Guide §6 describes `push_to_github.bat` auto‑merging after 300 s. File not in repo; auto‑merge
  contradicts Rule 20 ("floor, not a target") and Rules 10/13 (no self‑merge). §1 `Stop-Process -Name python`
  kills every python process. §2 cites `mistakes.py add` (real: `record`), Rule 31 (real: Rule 30),
  a ````mistake-ack` block that no tool knows. §3 cites Rule 31/33 (real: 31 only).

## Chunks (each = one commit + export + URL; mark ✅ + URL here in the same commit)
- [x] **C0** — this plan + `fixtures/human_msg_round14.txt` + `ROUND14_PREFLIGHT_AUDIT.md`. commit 50e9606 · URL: https://www.genspark.ai/api/files/s/AfBDOpPW
- [x] **C1** — commit 214ad46 · URL: https://www.genspark.ai/api/files/s/mq5nSG4O — `state_gate.py`: `open` (reads ai_state + PROGRESS, prints `state-open` block: head, state
      commit, drift N, next_action; exit 1 when drift>0 unless `--ack-drift`), `close [--write]` (turn_count+1,
      git_commit==HEAD, last_updated > open utc, next_action non‑empty; `--write` performs the update),
      `check <turn.md>` (first attested block = state_gate open, last = state_gate close, same head),
      `verify` (repo‑level: git_commit ∈ last 2 commits, PROGRESS.md exists), `--self-test`.
      attest grammar for `state_gate`. Rule 35.
- [x] **C2** — commit 6f7d17c · URL: (export lost in reset #2; content is inside every later archive) — `precheck.py` step 0 (`state_gate check`) ; `self_review.py` Q7 `state:` ; `Root/PROGRESS.md`
      created for real ; `ai_state.json` brought to HEAD by `state_gate close --write`.
- [x] **C3** — commit 1af78d7 · URL: (same) — pre‑commit hook "state moves with code" (staged files other than ai_state.json ⇒ ai_state.json
      must be staged and `state_gate verify --staged` exit 0) ; CI `state_gate verify` + `--self-test`
      (pending + live workflow).
- [x] **C4** — commit 1a644ea · URL: https://www.genspark.ai/api/files/s/ML4i1Ygy (the archive reset #2 was recovered from) — `mistakes.py recurrence`: a rule with ≥2 rows and no `escalation` row (`rule=<n>-ESC`)
      ⇒ exit 1. Rule 36.
- [x] **C5** — split: C5a commit d44a583 · URL: https://www.genspark.ai/api/files/s/9d29NdGQ ; C5b commit 75463b2 · URL: https://www.genspark.ai/api/files/s/kaEAS4ip — `edit_proof.py show --scope A-B`: parses `git diff -U0` hunks; any changed line outside
      [A,B] ⇒ `⛔ OUT-OF-SCOPE` exit 1 ; `mock_scan.py` (TODO / FIXME / `# ضع الكود` / `pass  # stub` /
      `return {"ok": True}` style constants / `NotImplementedError` in non‑abstract code) for staged files,
      in pre‑commit + CI. Rule 37.
- [x] **C6** — split: C6a (guide) commit ba74cc2 · URL: https://www.genspark.ai/api/files/s/y4X9hU7M ; C6b (rules/protocol/skills/plan) commit f4a6361 · URL: https://www.genspark.ai/api/files/s/SqJJGyeF ; C6c (review + handoff) _this commit_ — Guide corrections (§1 PID kill, §2 command + rule numbers, §3 real sub‑commands, §6 no auto‑merge,
      §8 table, §9 now points at state_gate) ; `AGENT_HARD_RULES.md` Rules 35‑37 ; `FULL_READ_PROTOCOL.md`
      steps ; 7 skills bumped ; `ROUND14_REVIEW.md` (`req_coverage --full`) ; `HANDOFF_ROUND14.md`.
- [ ] **C7** — squash to one commit + final export URL. Owner pushes `-f` + opens PR. No self‑merge.

## Turn contract
- Every fact = tool block with ATTEST footer (Rule 21). No typed verdicts (Rule 29).
- "pushed/updated" only after `remote_proof.py` says REMOTE — expected ❌ all round (no credential).
- Chunk ≤ 3 files, ≤ 150 lines, one self‑test command.
- From C2 onward every turn starts with `state_gate open` and ends with `state_gate close --write` (Rule 35).
