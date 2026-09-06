# Round 13 — Frozen plan (written FIRST, before any tool work — Rule 11)

Source of truth for this round. After a sandbox reset: open this file, run `git log --oneline -8`,
resume from the first chunk without ✅. Never rebuild from memory.

## Reset log
- Reset #1 (prev session): Round‑13 work reached local commit `dd8728c` (precheck/self_review/edit_proof/mistakes
  + Rules 30‑34). **Never left the sandbox** — no credential to push, no export uploaded. Lost entirely.
- Reset #2 (this session, 2026‑09‑06): `/tmp` wiped, checkout is a fresh clone of `main` @ `1fffe4d`.
  `git cat-file -t dd8728c` → "Not a valid object name". AI Drive read‑only. `setup_github_environment` → no token.

**Status of every finding/design below: RECONSTRUCTED** from the previous session's turn draft (which the human saw)
— not from a gist or file. Human corrects → this file is amended in the same commit as the fix.

## Off‑sandbox rule for this round (push substitute)
Each chunk = `git commit` → `sh .governance/export_bundle.sh` → upload archive → paste URL in the row below.
A chunk without a URL is NOT done (Rule 11). Owner applies: `tar xzf …; git am 0*.patch; git push origin genspark_ai_developer`.

## Findings (RECONSTRUCTED)
- **R85** — Agent admitted a mistake in prose ("I was wrong / غلطت") with no record anywhere; the same class of
  mistake recurred next round. Gap: admissions are not logged.
- **R86** — Agent wrote "edited / عدّلت X" with no diff or hash proving the edit happened on that file.
- **R87** — Agent's self‑critique block never contained a ❌; every answer was ✅ (decoration).
- **R88** — Agent sent turns without running the checkers on the turn text itself; violations were found by the
  human, after the fact.
- **R89** — Round‑13 chunks were built for ~40 min with no export; reset destroyed them (R39 repeat, Rule 11 breach).

## Chunks (each = one commit + export + URL; mark ✅ + URL here in the same commit)
- [x] **C0** — this plan + `fixtures/human_msg_round13.txt` + HANDOFF_ROUND13 stub. commit f2c1c72 · URL: https://www.genspark.ai/api/files/s/TFDXSmP2
- [x] **C1** — `mistakes.py` (+ attest grammar, MISTAKES.md seeded). commit bf8527d · URL: https://www.genspark.ai/api/files/s/VBYtS8CC —: `check <turn.md>` — an admission phrase (`غلطت|كنت مخطئ|I was wrong|my mistake|
      خطأ مني`) requires a `MISTAKES.md` row appended in the same commit (`| date | round | what | rule |`);
      `record` appends the row. Self‑test. Rule 30.
- [x] **C2** — `edit_proof.py` (show/check; mode-only chmod ≠ edit; + attest grammar). commit 745c24e · URL: https://www.genspark.ai/api/files/s/FlMZAtbq —: `check <turn.md>` — an edit claim (`عدّلت|أصلحت|edited|fixed|patched <path>`)
      requires a ```edit-proof block (`git diff --stat` + `git rev-parse HEAD` for that path) with ATTEST footer.
      Self‑test. Rule 31.
- [x] **C3** — `self_review.py` (S1-S7; + attest grammar). commit 7b550b7 · URL: https://www.genspark.ai/api/files/s/YqAQ2Nok —: `check <turn.md> --human <msg>` — requires a ```self-review block with Q1‑Q6
      (attested / prechecked / skipped / pleasing / re‑read / remote), each with ✅/❌ + evidence; S1‑S6 checks
      incl. S5 (Q5 `missed:` quote verbatim in human msg) and "at least one ❌ or an explicit `none: <why>`".
      Self‑test. Rule 32.
- [x] **C4** — commit edb8315 · URL: https://www.genspark.ai/api/files/s/J3kbyjWl — (edit_proof self-test fixed for the committed-file case) `precheck.py <turn.md> --source <human>`: runs intent_gate → attest → claim_check → read_proof →
      edit_proof → mistakes → self_review → req_coverage in order, stops at first exit≠0, prints the table.
      `attest.py` grammar: `precheck`, `self_review`, `edit_proof`, `mistakes`. Self‑test. Rule 34.
- [x] **C5** — commit 51ac939 (re-applied after reset #3; orig 319f69d) · URL: https://www.genspark.ai/api/files/s/RCPmtSy9 — (also mirrored into live `.github/workflows/governance-gate.yml`; step passes locally exit 0) `AGENT_HARD_RULES.md` Rules 30‑34 (30 admissions logged, 31 edit‑proof, 32 self‑review must be able
      to say ❌, 33 export‑before‑next‑chunk is part of the chunk, 34 precheck before send); `FULL_READ_PROTOCOL.md`
      steps; `pending/governance-gate.yml` self‑test step for the 4 new tools.
- [x] **C6** — split after reset #3 wiped the monolithic C6 mid-commit:
  - [x] **C6a** skills bump ×7 + MISTAKES row 3. commit 8a80079 · URL: https://www.genspark.ai/api/files/s/g8b2WxWf
  - [x] **C6b** `ROUND13_REVIEW.md` (req_coverage --full 134/134, 4 REQ). commit 774a2a0 · URL: https://www.genspark.ai/api/files/s/amWgTVpW
  - [x] **C6c** `HANDOFF_ROUND13.md` final (chunk table, verify + apply commands). commit 27fad5a · URL: https://www.genspark.ai/api/files/s/7rPn3A6B
- [x] **C7** — squashed into ONE commit (9 → 1); final archive URL: https://www.genspark.ai/api/files/s/gH1s1jgW (pre-amend 7cb597a; the post-amend re-export is listed in the last chat message and in HANDOFF). Owner pushes + opens PR (credential‑blocked; commands in HANDOFF).

## Turn contract
- Every fact = tool block with ATTEST footer (Rule 21). No typed verdicts (Rule 29).
- "updated/saved/pushed" only after `remote_proof.py` says REMOTE (Rules 18/25) — expected ❌ all round.
- Chunk ≤ 3 files, ≤ 150 lines, one self‑test command (skill Rule 30 micro‑task).
