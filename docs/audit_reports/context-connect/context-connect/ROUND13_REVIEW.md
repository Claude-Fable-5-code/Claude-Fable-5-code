# ROUND 13 REVIEW — "continue from the last point; the sandbox reset again; push-per-chunk"

Fixture: `fixtures/human_msg_round13.txt` (134 non-space chars). Intent gate: `MODE: EXECUTE` — the message is a resume order with the method named (small chunks, each pushed). This file was itself lost once (reset #3, mid-C6) and rebuilt from the C5 archive; that loss is MISTAKES.md row 3.

```req-ledger
SENTENCES: 4
COVERAGE: 4 REQs from 4 sentences — none skipped; --full: every remaining character is a LEFTOVER line below
REQ-01 [ASK]  "تابع من اخر نقطه" → §1 — resumed from the last exported archive (C5 URL), not from memory; `git log` shape decides what remains
REQ-02 [ASK]  "اوعي تنسي ده Sandbox reset مجددًا" → §2 — three resets this round; the standing failure is "work that never left the sandbox" (R89, Rule 33)
REQ-03 [ASK]  "أستعيد وأجمّد الخطة فورًا" → §3 — PLAN_ROUND13.md is the first commit and the only checklist; restored verbatim from the archive, ticks + URLs unchanged
REQ-04 [ASK]  "ثم أنفّذ بchunks صغيرة مدفوعة (push-per-chunk لمقاومة الـresets)" → §4 — no push credential exists; "pushed" = exported archive + URL, run in the same command as the commit
LEFTOVER [SEPARATOR] "... ........."
LEFTOVER [SEPARATOR] "."
LEFTOVER [SEPARATOR] ":"
```

## §1 — Resume from evidence, not memory (REQ-01)
After every reset the first command is `git log --oneline` + `ls /tmp` + `grep -c "Round 13" .agents/skills/*/SKILL.md`. Reset #3 showed: branch `main` only, no `/tmp` archives, no skills bump — so C0‑C5 came back from the C5 URL (`git am 0*.patch`) and C6 was redone as C6a/C6b/C6c.

## §2 — Findings R85‑R89 (RECONSTRUCTED; each is a tool, not a promise)
| finding | shape | mechanical answer |
|---|---|---|
| R85 | "I was wrong" in prose, forgotten next session | `mistakes.py record/check` + `MISTAKES.md` (Rule 30) |
| R86 | "edited X" with no diff shown | `edit_proof.py show/check` (Rule 31) |
| R87 | self-critique that is always all-✅ | `self_review.py` six fixed questions; ✅ on Q6 without REMOTE proof fails (Rule 32) |
| R88 | checkers run by the human after sending | `precheck.py <turn> --source <human>` before sending; its sha is Q2 (Rule 34) |
| R89 | 40 min of chunks, zero exports, reset wiped them | Rule 33 export-per-chunk; no URL, no tick |

## §3 — Freeze the plan (REQ-03)
`PLAN_ROUND13.md` is commit C0. Nothing is re-planned after a reset; only the checkbox state advances. Each row carries its commit SHA and its archive URL; a row without a URL is not done, whatever the local log says.

## §4 — "push-per-chunk" without a credential (REQ-04)
`setup_github_environment` → "No Valid GitHub Authorization Found" on every attempt this round. So the operative form of "مدفوعة" is: `git commit && sh .governance/export_bundle.sh` **in the same shell command**, then upload, then the URL goes into the plan. Reset #3 hit between commit and export once — which is why the two are now one command.

```req-closure
REQ-01 DONE      C0-C5 restored from https://www.genspark.ai/api/files/s/RCPmtSy9 ; C6a exported https://www.genspark.ai/api/files/s/g8b2WxWf
REQ-02 DONE      MISTAKES.md rows 1-3 (resets #1-#3) https://www.genspark.ai/api/files/s/g8b2WxWf
REQ-03 DONE      PLAN_ROUND13.md unchanged since C0 except ticks/URLs https://www.genspark.ai/api/files/s/RCPmtSy9
REQ-04 BLOCKED   no GitHub credential in sandbox; export-per-chunk substituted (Rule 33); owner pushes via HANDOFF_ROUND13 commands
UNMAPPED: none
```
