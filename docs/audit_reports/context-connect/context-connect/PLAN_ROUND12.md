# Round 12 — Frozen plan (push-per-chunk; sandbox resets wipe /tmp and uncommitted work)

Source of truth for this round. If the sandbox resets, re-read THIS file, run `git log --oneline -8`,
and continue from the first chunk not marked ✅ below. Never rebuild from memory.

## Findings this round (from gist 8ac3ca02 + the human's Round-12 message)
- **R81** — Agent *typed* a checker verdict line (`✅ claim_check: prose consistent with 2 tool block(s)`)
  in prose, with no ATTEST footer, under a turn that claim_check actually scores 15+ contradictions.
- **R82** — Agent claimed `PROGRESS.md` / `ai_state.json` "updated" with no `remote_proof` block (Rule 18/25 repeat).
- **R83** — Human asked "قبل ما تبحث عن حاجه تتاكد فعلا انك فاهم كلامي … مش تخمن"; agent went straight to
  grep/edit. No plan-only trigger existed, so `intent_gate` said ACT. Gap: a standing *mirror-before-act* request.
- **R84** — Human's core complaint: "بيكون منك تخمين و مش بتشوف سكربت كامل للنهايه". Diagnoses are guessed from
  partial reads. Gap: no artifact proves the file was read end-to-end before a bug/cause is named.

## Chunks (each = one commit + `git push`; mark ✅ here in the same commit)
- [x] **C0** — this plan file. *(committed with the branch reset)*
- [x] **C1** — `intent_gate.py`: CONFIRM-FIRST mode (CONFIRM_TRIGGERS + AMBIGUITY lists, `detect_confirm`,
      `verify_confirm` requiring a ```mirror block with `UNDERSTOOD:` verbatim quotes + `WAITING FOR:` and zero
      action markers). Self-test on the real Round-12 message. Rule 27.
- [x] **C2** — `claim_check.py`: **C7** typed-verdict detector (`✅/⛔ claim_check:|attest:|req_coverage:|read_proof:|
      intent_gate:|ci_status:|remote_proof:|merge_pr:` or `MODE: …` in prose). Self-test. Rule 29.
- [x] **C3** — `read_proof.py` (new): `index <file>` emits a ```read-proof block (FILE/LINES/SHA256 + INDEX of every
      def/class/section with line numbers); `check <turn.md>` fails a turn that names a bug/cause/fix
      ("the bug is / السبب / الخطأ في / غلط في") without a read-proof block whose LINES equals `wc -l` and whose
      SHA256 matches. Self-test. Rule 28.
- [x] **C4** — `attest.py`: register `read_proof` grammar; widen claim_check grammar to `C[1-7]`.
      Fixtures: `agent_gist_round12.md` (fetch gist 8ac3ca02 if reachable; else reconstruct the 3 turns from
      HANDOFF notes and mark RECONSTRUCTED), `agent_turn3_round12.md`.
- [x] **C5** — `AGENT_HARD_RULES.md` Rules 27-29; `FULL_READ_PROTOCOL.md` steps for mirror + read-proof;
      `.governance/pending/governance-gate.yml` gains "checker family self-tests" step with R81/R83/R84 negatives
      (workflow dir is owner-applied, see pending/README.md).
- [x] **C6** — `HANDOFF_ROUND12.md`, `ROUND12_REVIEW.md`, `.agents/skills` bump if present; squash → PR → share link.

## Turn contract for the rest of this round
- Every fact = tool block with ATTEST footer (Rule 21). No typed verdicts (Rule 29).
- "updated/saved" only after `remote_proof.py` (Rule 18/25).
- If the human's message is CONFIRM-FIRST → ```mirror block only, then wait for "تمام".
