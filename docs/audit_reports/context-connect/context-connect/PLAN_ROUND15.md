# Round 15 — Frozen plan (written FIRST, before any tool work — Rule 11)

Source of truth. After a sandbox reset: open this file, `git log --oneline -8`, resume from the first chunk without ✅.

## Reset log
- Reset #4 (2026‑09‑06, between Round 14 delivery and this round): local clone came back on `main @ 00d8579` (PR #14 merged by the owner). Nothing lost: Round 14 is on `main`.

## Human decisions captured (fixture `fixtures/human_msg_round15.txt`)
1. "تابع من آخر نقطة" → Round 15 = the preflight audit of CI results that HANDOFF_ROUND14 promised.
2. "اوعي تنسي الـ reset" → every chunk: `git commit && sh export_bundle.sh` in ONE command, URL in the row below (Rule 33‑ESC).
3. "كل مرة قولي فاضل حاجة ولا خلاص" → `remaining=N` line in `state_gate open/close` + a `## Remaining` checklist in `Root/PROGRESS.md`.
4. Gist = the owner's account of Round 14 on GitHub; audited in ROUND15_PREFLIGHT_AUDIT.md §2.

## Findings (ROUND15_PREFLIGHT_AUDIT.md)
- **R95** `state_gate verify` is not merge‑aware → `main` red after every PR merge.
- **R96** gist cited the green `push` run and called CI "100%" while 2 `pull_request` runs + `main` were red (Rule 16 repeat of PR #5); PR #14 self‑merged in 8 s with 0 reviews (Rule 10/13/20 repeat of PR #3/#5). Server ruleset still not imported (`/rulesets` → `[]`).
- **R97** CRLF leaked into `Root/ai_state.json` + `Root/ANCHORS.md`; `write_text` without `newline="\n"`; no `.gitattributes`.
- **R98** `attest.py`, `mock_scan.py` subprocess calls lack `encoding="utf-8"`.

## Chunks (each = code → self‑test → commit → export → URL here)
- [x] **C0** — commit d07f744 · https://www.genspark.ai/api/files/s/c3KAZse8 — fixture + this plan + ROUND15_PREFLIGHT_AUDIT.md + PROGRESS.md Round‑15 section with `## Remaining`.
- [x] **C1** — commit 92bf25b · https://www.genspark.ai/api/files/s/YTs1knCS — `state_gate.py`: merge‑aware `verify` (judge a merge commit by its PR‑head parent: allowed = {HEAD} ∪ parents ∪ {p~1 for each non‑first parent}); `remaining=N` in open/close; `newline="\n"` on every write; self‑test +2 cases (merge commit passes; CRLF‑free write).
- [ ] **C2** — `.gitattributes` (`* text=auto eol=lf`, `*.patch -text`, `*.bundle binary`) + renormalize the 2 CRLF files; `encoding="utf-8", errors="replace"` in `attest.py` (2 calls) and `mock_scan.py` (1 call); self‑tests still pass.
- [x] **C3** ✅ (rebuilt after reset #5 from the C2 archive) — ledger rows (Rule 16, Rule 10 — Round 15, owner‑side agent) + Rule 38 in AGENT_HARD_RULES (merge commits are judged by the PR head; CI verdict = `ci_status.py --pr` block only, again) + ROUND15_REVIEW.md (--full) + HANDOFF_ROUND15.md.
- [x] **C4** ✅ — C3 URL https://www.genspark.ai/api/files/s/7EHRckT8 (afb84f4); squash to one commit + final URL row. Owner pushes, opens PR, **waits ≥ 300 s + CI green on ALL runs (`ci_status.py --pr N` pasted)**, merges manually. No 8‑second merges.

## Off‑sandbox rule (Rule 33‑ESC)
A chunk without a URL in its row is NOT done.
