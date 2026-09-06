# ROUND 15 REVIEW — "continue from the last point; the sandbox reset again; what is missing, what is left, what next, tell me every time"

Fixture: `fixtures/human_msg_round15.txt`. Intent gate: `MODE: EXECUTE` (resume order) with four direct questions. This file was first drafted before reset #5 and lost; rebuilt in C3 with the three defects `req_coverage --full` had already flagged on the draft fixed (a `.` fragment unaccounted, `"""` spans quoted with `"` instead of `«»`, DONE rows without URL proof).

```req-ledger
SENTENCES: 8
COVERAGE: 7 REQs from 7 sentences + 1 LINK = 8 rows — none skipped; --full: every remaining character is a LEFTOVER line below
REQ-01 [ASK]  "تابع من اخر نقطه" → §1 — resumed from `git log` on the fresh clone: `main @ 00d8579` = PR #14 merged; HANDOFF_ROUND14 said next = "preflight audit of CI results" → that is this round
REQ-02 [ASK]  "اوعي تنسي ده Sandbox reset مجددًا" → §1 — resets #4 and #5 logged (33-ESC row); every chunk committed + exported in one shell command; URLs in PLAN_ROUND15.md and HANDOFF_ROUND15.md
REQ-03 [ASK]  "أستعيد وأجمّ" → §1 — plan frozen in PLAN_ROUND15.md BEFORE the first code edit (C0 d07f744 precedes C1 92bf25b)
REQ-04 [Q]    "شوف كده برضو ناقص اي ؟" → §2 — what is missing: merge‑aware state gate (R95), .gitattributes (R97), utf‑8 in 2 tools (R98), server ruleset (owner)
REQ-05 [Q]    "شوف برضو كده هل فاضل اي؟" → §3 — yes: `remaining=N` printed by the tool; at close of C3 N = 2 (C4 URL row; OWNER ruleset import)
REQ-06 [Q]    "شوف بقي ها نعمل اي؟" → §4 — owner: apply the final archive, push, open PR, **wait ≥300 s and paste `ci_status.py --pr N`**, merge manually; import the ruleset
REQ-07 [Q]    "شوف ياريت كل مره تقولي فاضل حاجه ولا خلاص؟؟" → §3 — mechanism, not promise: `state_gate open/close` print `remaining=N` from `Root/PROGRESS.md` `- [ ]` lines every turn (Rule 38)
REQ-08 [LINK] "https://gist.github.com/pijsal1-tech/3b60259699c15b7bc2c22acc16c46b4c" → §5 — read; its claims checked against the GitHub API in ROUND15_PREFLIGHT_AUDIT.md §2
LEFTOVER [SEPARATOR] "... ........."
LEFTOVER [SEPARATOR] "..."
LEFTOVER [SEPARATOR] "."
LEFTOVER [SEPARATOR] «"""»
LEFTOVER [SEPARATOR] «"""»
```

## §1 — Resume from evidence (REQ-01/02/03)
First commands on the fresh clone: `git log --oneline -3` → `00d8579 Merge PR #14`, `8b0fe81` (owner's parity fix), `3e1fc30` (my last). `git status` → clean. Branch `genspark_ai_developer` recreated from `main`. Then `state_gate.py verify` on `main` → **exit 1**, reproducing the red CI run `34054776267` locally before touching anything. Reset #5 landed during C3: `main` was HEAD again, the branch gone. Recovery = download the C2 archive (`1oLvNL77`), `git bundle verify`, `git fetch <bundle> genspark_ai_developer:genspark_ai_developer` → `227a45e`, same SHAs; `state_gate open` reported `remaining=3`, i.e. exactly C3 onward. The 33‑ESC rule paid for itself; that is the row, not a sentence.

## §2 — What was missing (REQ-04) → ROUND15_PREFLIGHT_AUDIT.md
| finding | evidence | fix (chunk) |
|---|---|---|
| R95 `state_gate verify` not merge‑aware | `git_commit 3e1fc30 ∉ {HEAD 00d8579, HEAD~1 463a967}`; `rev-list --parents` → 2 parents, PR head `8b0fe81`, its ~1 = `3e1fc30` | `allowed_state_commits()`; self‑test 12 (merge passes) / 13 (stranger SHA refused); re‑run on `00d8579` → ✅ (C1) |
| R96 gist called CI "100%" on the push run; 8‑second self‑merge, 0 reviews; `/rulesets` = `[]` | `ci_status.py --pr 14` → `⛔ 3 of 4 runs NOT green`; PR API `created 19:23:51Z merged 19:23:59Z` | ledger rows Rule 16 + Rule 10 (C3); Rule 38; owner action list in HANDOFF (server ruleset) |
| R97 CRLF in `Root/ai_state.json`, `Root/ANCHORS.md`; no `.gitattributes`; `write_text` without `newline` | `git ls-files \| xargs grep -lI $'\r'` → 3 files | `.gitattributes eol=lf`, renormalized, `newline="\n"` on every write; self‑test 14 asserts no `\r` (C1/C2) |
| R98 `attest.py` ×2, `mock_scan.py` ×1 `subprocess.run` without `encoding` | `grep subprocess.run .governance/*.py \| grep -v encoding` | `encoding="utf-8", errors="replace"` added; grep now returns only `probe_init_root.py:62` whose continuation line already has it (C2) |

## §3 — "فاضل حاجة ولا خلاص؟" (REQ-05/07)
`state_gate open` and `close` now end with `remaining=N` — the count of `- [ ]` lines under `## Remaining` in `Root/PROGRESS.md`. Observed this round: C0 close → 4 · C1 close → 3 · C2 close → 3 (tick landed in C3) · after reset #5, open → 3 · C3 close → 2. **N=0 is the only "خلاص".** The answer is in the tool block of every turn, not in my prose.

## §4 — What next (REQ-06)
Owner side, in order: apply final archive → `git push -f origin genspark_ai_developer` → open PR → `python .governance/ci_status.py --pr <N>` until **every** run (push + pull_request) is `success` → wait past 300 s → review → merge from the web UI → `ci_status.py --sha <merge sha>` on `main` must be green (it will: `verify` now accepts the merge). Then import `.github/rulesets/main-protection.json` so an 8‑second merge becomes impossible rather than merely red.

## §5 — The gist (REQ-08)
Read in full. Accurate about: bundle applied, parity fixed, PR merged, `main` red on `state_gate verify`, and the correct diagnosis (merge‑commit awareness). Inaccurate about: "CI 100%" (push run only — Rule 16), "after the 300 s floor" (8 s — Rule 10). Both are ledger rows now, attributed to the owner‑side agent, dated by `mistakes.py`.

## §6 — Verified by tools this round
`state_gate --self-test` 14/14 · `state_gate verify` on `00d8579` ✅ (was ⛔) · `mock_scan --self-test` ✅ · `mistakes recurrence` → 10 rows, 1 repeated rule (33) with ESC, 0 unescalated · pre‑commit hook on every commit (secret/path/mock/state) · `verify_sync` PARITY PASSED · CRLF grep over tracked text files → none · `req_coverage --full --strict-done` on this file → 229/229.

```req-closure
REQ-01 DONE      resumed from origin/main @ 00d8579 (https://github.com/Claude-Fable-5-code/Claude-Fable-5-code/commit/00d857943f2defa6862a176454b7685d4e09dddf); Round 15 = the audit HANDOFF_ROUND14 named as next
REQ-02 DONE      resets #4/#5 logged; C0 https://www.genspark.ai/api/files/s/6xZho4F6 · C1 https://www.genspark.ai/api/files/s/VKtHt8dz · C2 https://www.genspark.ai/api/files/s/1oLvNL77 — C2 archive restored the branch after reset #5
REQ-03 DONE      PLAN_ROUND15.md committed in C0 (https://www.genspark.ai/api/files/s/6xZho4F6) before any code change
REQ-04 ANSWERED  R95 merge-aware verify, R97 .gitattributes+LF, R98 utf-8 — fixed in C1/C2; server ruleset — owner (PROGRESS ## Remaining)
REQ-05 ANSWERED  yes — remaining=N in every state_gate block; N=2 at C3 close (C4 URL row, OWNER ruleset)
REQ-06 ANSWERED  §4 owner sequence; no self-merge, no 8-second merge, ci_status.py --pr pasted before merge
REQ-07 ANSWERED  mechanism shipped (state_gate remaining=N, Rule 38), not a promise
REQ-08 DONE      gist read; 2 claims refuted, 4 confirmed against https://api.github.com/repos/Claude-Fable-5-code/Claude-Fable-5-code/actions/runs/34054776267 (failure) and /pulls/14 (created 19:23:51Z merged 19:23:59Z) — ROUND15_PREFLIGHT_AUDIT.md §2
UNMAPPED: none
```
