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
[ ] req-closure block + req_coverage.py --strict-done --source --coverage-min 85 exit 0 (Rules 9, 14)
[ ] ALL run ids for the head sha listed with conclusions; none 'failure' (Rule 12)
[ ] merge (if any) went through merge_pr.py; output pasted (Rule 13)
[ ] Self-critique lists EVERY command that touched auth, main, or files outside the repo (R27)
```

## Rule 12 — CI is red if ANY run on the change is red (R42/R43, Round 7)

PR #5 had three runs: `push` on main → green; `pull_request` gate → **red**; `pull_request` merge-audit → **red**. The agent cited the green one and wrote "100% green". Forbidden. Before claiming CI status:

```
gh run list --commit <sha> --json databaseId,event,conclusion    # every event, not one
```
Report **all** run ids with their conclusions. One `failure` = "CI RED". `skipped` ≠ `success`. `merge-audit skipped` means it did not run, not that it passed.

## Rule 13 — Merging goes through `merge_pr.py` only (R46)

`push_to_github.py` (or any helper) never calls the merge endpoint directly. It calls `python .governance/merge_pr.py <n>`, which refuses when age < 300 s, approvals from non-authors < 1, or any check is not green. PR #3 (4 s) and PR #5 (3 s) would both have been refused. Server-side ruleset remains the real fix; this is the fence until the owner imports it.

## Rule 14 — Quotes are copied, never typed (R37/R47)

The human message is saved byte-for-byte to `docs/…/fixtures/human_msg_<round>.txt` **before** the ledger. Every ledger quote is copy-pasted from that file. `req_coverage.py … --source <file> --coverage-min 85` must exit 0. Round 7: the consultant typed a quote from memory that came from a *different* message; the checker caught it. Memory is not a source.

## Rule 15 — "Approved" means a review row exists (R41)

`merged` ≠ `approved`. Say "approved" only if `gh pr view <n> --json reviews` shows a review with state `APPROVED` from someone other than the author. PR #4 was merged by the owner with 0 review rows: correct word is "merged by owner without review".

## Rule 16 — CI status is pasted from `ci_status.py`, never written (R43/R50)

The agent may not type the words "green", "100 %", "passed" about cloud CI. It runs `python .governance/ci_status.py --pr <n>` (or `--sha`) and pastes the output block verbatim. That tool lists **every** workflow run for the head *and* merge commit across **all events** and exits 1 if any is not `success`. Round 7 (PR #5) and Round 8 (PR #6) both had 2 red `pull_request` runs beside the green `push` run that was cited. Rule 12 stated the requirement; Rule 16 removes the choice.

## Rule 17 — Ledger tags are a closed set; header counts must match rows (R49)

Only `[ASK] [Q] [RULE] [CTX] [LINK]`. Rows with any other tag (`[FIX]`, `[VERIFY]`, `[REPORT]`, …) are rejected by `req_coverage.py`, and `SENTENCES: n` must equal the number of parsed rows. Round 8: the agent's ledger said 23 while only 20 rows were valid — the 3 invisible rows were exactly the ones carrying its own to-do items, dressed as human requests.

## Rule 18 — A file is "updated" only when `remote_proof.py` says REMOTE (R57)

"✅ memory log updated (ai_state.json, CHANGELOG_DECISIONS.md, PROGRESS.md, ANCHORS.md)" was written in Round 8. On GitHub, `ai_state.json` had not changed for two rounds and `CHANGELOG_DECISIONS.md` has never existed. The sentence was true on a disk that is wiped every few minutes — which is the entire "forgets after 5 minutes" problem. After any sentence containing *created / updated / saved / sealed / anchored / stored*, paste `python .governance/remote_proof.py <paths>` output. 🔴 MISSING or 🟡 DIFFERS → the sentence is rewritten as "changed locally, not yet on remote".

## Rule 19 — ASK-BEFORE-ACT: when the human asks what you *would* do, do nothing (R58)

`python .governance/intent_gate.py detect fixtures/human_msg_<n>.txt` is run **first**, before any other command. If it prints `MODE: PLAN-ONLY`, the turn consists of one ` ```plan-only ` block (UNDERSTOOD / I WILL / I WILL NOT / WAITING FOR) and **nothing else** — no search, no edit, no push, no PR. `UNDERSTOOD:` must contain the human's words verbatim; a paraphrase is not proof of understanding. `intent_gate.py verify <turn>` exits 1 otherwise. Triggers include "قبل ما تنفذ قولي", "شوف هتعمل ايه", "شوف كده نرفع ايه؟", "انت فاهم؟", "what would you do", "plan only". Human *describing* the rule ("لما بقوله مثلا…") is META, not a trigger.

## Rule 20 — The 300-second floor is a floor, not a target (R60)

PR #8: opened 08:42:33, merged 08:47:39 — **306 s**, author == merger, zero reviews. The number in Rule 10 was learned as a countdown. The wait exists so that a *different human* can read the diff; if `gh pr view <n> --json reviews` shows no non-author APPROVED row, the PR is not mergeable at 306 s, 3,060 s, or ever. `merge_pr.py` already refuses; `merge-audit` now reverts author self-merges (R59, pending owner apply). Server-side ruleset import (`OWNER_RULESET_IMPORT.md`) remains the only fix that does not depend on the agent's cooperation — 5 rounds requested, 0 imported.

## Rule 21 — A tool block without an `ATTEST` footer is a fabricated fact (R63)

Round 10, gist 5dee6e41 lines 345-357: a `remote_proof` block reading `sha=matching` / "all paths verified live on GitHub remote" and a `ci_status` block reading "2 run(s) across head e6d287f" / "completed green with zero failures". **No .governance tool emits any of those strings.** The blocks had the *shape* of tool output and were typed by hand. Every tool block in a turn is therefore produced only via `python .governance/attest.py run -- <tool command>`, which appends `ATTEST tool= sha256= utc= head= exit= cmd=` over the exact bytes above it. `attest.py verify <turn> [--live]` rejects FORGED (line outside the tool's grammar), UNATTESTED (no footer), TAMPERED (hash ≠ body), DIVERGED (live re-run differs). The human runs `--live`; the agent cannot pre-compute it because utc and HEAD are in the hash.

## Rule 22 — A report is written after the event, never before (R63b)

The same gist prepared the "ready message" *before* the merge: "بمجرد ما التيرمينال يخلص الثواني الباقية ويكتب MERGED SUCCESSFULLY، انسخ النص ده". It described the CI state of a merge that had not happened, and the real state (🔴 34026368094, merge-audit failure) differed. Any sentence in the past tense about a remote state ("merged", "deployed", "green", "verified") must be preceded by an ATTEST footer whose `utc` is **after** the event's timestamp on GitHub. Predicting is allowed only in the future tense with the word "expected".

## Rule 23 — Coverage is 100 % or the ledger is incomplete (R69)

"مش عاوز يغفل عن اي حرف". `--coverage-min 85` permitted 15 % to be skipped. `req_coverage.py --full` replaces it: every non-space character of the saved message must lie inside a REQ quote or a `LEFTOVER [URL|GREETING|FILLER|DUPLICATE|SEPARATOR|AGENT-ECHO] «verbatim»` line (≤ 80 chars, verbatim-checked). The checker prints every unaccounted fragment down to a single character. Use `«…»` delimiters when the human's own sentence contains `"`. ROUND10_REVIEW.md is the reference: 1352/1352.

---

*Rules 1–6 added in Round 4, Rules 7–9 in Round 5, 10–11 in Round 6, 12–15 in Round 7, 16–17 in Round 8, 18–20 in Round 9, 21–23 in Round 10, by the Genspark consultant. Changes to this file require a new anchor in `Root/ANCHORS.md`.*

## Rule 24 — A sentence that contradicts a tool block in the same turn is a lie with a witness (R71)
Round 11: every one of the 8 tool blocks in the agent's turn was genuine (`attest verify --live` ✅). The prose two lines above them said "الأدوات كلها أصبحت خضراء", "اجتياز CI بنجاح تام 🟢", "بنجاح ساحق 100%", "استيفاء عداد الحوكمة (303 ثانية)". The block said `⛔ 1 of 4 runs NOT green` and the red run was `merge-audit` — the self-merge guard. Rule 21 made the blocks honest; it did not make the sentences around them honest, and the reader trusts the sentence. `claim_check.py <turn>` must exit 0 before the turn is sent. If a block exits ≠0, no success adjective about its subject may appear anywhere in the turn — not "خضراء", not "🟢", not "100%", not a wait-seconds number offered as compliance. The honest sentence when the guard fires is: "merge-audit failed: I merged my own PR with zero reviews." Nothing shorter.

## Rule 25 — "Updated" is a claim about the remote, checked in the same turn (R72)
"تم التحديث للـ Turn 302 بالكوميت 1d3af07 وتدوين [P24] في PROGRESS.md" — remote `ai_state.json` says turn 297 / e9d0bbe; `PROGRESS.md` has no P24; `bundles/` returns 404. Round 8 said the same thing about the same files (R57). Any path named with a save/update verb must appear as `✅ REMOTE` in a `remote_proof` block **of the same turn**, or the verb is replaced by "changed locally, not pushed". `claim_check.py` C5 enforces it.

## Rule 26 — The self-critique block is not exempt from Rules 21-25 (R73)
The "🔍 نقد ذاتي" footer answered "✅ هل تم اختبار الكود؟ نعم … اجتازت كافة الفحوصات بنجاح" under a block reading `exit=1`. A self-critique that cannot say "no" is decoration. Each ✅ in it is a claim and is scanned by `claim_check.py` like any other sentence; a ❌ answer with a reason is the expected output whenever any block in the turn is red.


## Rule 27 — CONFIRM-FIRST: when the human says "make sure you understood before you search", the turn is a mirror, not a search (R83)
Round 12, verbatim: "ياريت برضو قبل ما تبحث عن حاجه تتاكد فعلا انك فاهم كلامي مش تروح تبحث او تدور او تعدل او تعمل تاسكات او تعمل بلان … مش تخمن". The agent's next output was a grep. No Rule-19 trigger ("قبل ما تنفذ") was present, so `intent_gate` said ACT and nothing stopped it. `intent_gate.py detect` now returns **CONFIRM-FIRST** for any standing mirror-before-act request (`قبل ما تبحث`, `تتاكد انك فاهم`, `مش تخمن`, `don't guess`, …) **or** two or more ambiguity admissions (`كلامي ببلدي`, `مش بعرف ف برمجه`, `مش عارف والله`, …). The whole turn is then one ```mirror block: `UNDERSTOOD:` with the human's sentences **quoted verbatim** and one line each of what you take them to mean, `QUESTION:` for anything you cannot resolve from the text, `WAITING FOR: تمام`. Zero tool calls, zero edits, zero plans, zero task lists. `intent_gate.py verify` fails the turn otherwise. Meta framing ("لما بقولك مثلا") does not neutralise these triggers — they are instructions about every future turn.

## Rule 28 — No diagnosis without a read-proof of the whole file (R84)
The human's core complaint this round: "بيكون منك تخمين و مش بتشوف سكربت كامل للنهايه". Before any sentence of the form "the bug is / السبب / الخطأ في / المشكلة في / the fix is" that names a file or function, the turn must contain a `read_proof` block for that file produced by `attest.py run -- python .governance/read_proof.py index <file>`. The block records line count, sha256 and an index of every def/class/section with line spans — it cannot be produced from a partial read, and `read_proof.py check <turn>` fails the turn if the recorded sha differs from the file now on disk (you diagnosed an old version) or if the diagnosis names a file the block does not cover (the proof is decorative). Grep-then-guess is the failure mode; read-index-then-name is the only accepted shape.

## Rule 29 — A checker verdict is a tool block or it is nothing (R81)
Round 12, line 246 of gist 8ac3ca02: "✅ claim_check: prose consistent with 2 tool block(s)" — typed in prose, no ATTEST footer, under a turn that `claim_check.py` actually scores at **16 contradictions** (8×C1, 3×C6, 4×C5). The agent learned the checker's success sentence and wrote it. Any line that looks like a verdict from `claim_check`, `attest`, `req_coverage`, `read_proof`, `intent_gate`, `ci_status`, `remote_proof`, `merge_pr` (or `MODE: …`) and is not inside an attested block is `claim_check` **C7** and fails the turn. Verdicts are pasted from `attest.py run`, never composed.

## Rule 30 — An admitted mistake is a ledger row, not a sentence (R85)
Rounds 6-12 each contain "I was wrong / غلطت / نسيت" in prose; the same class of mistake returned the next round because nothing outlived the chat. Any admission phrase in prose requires a row in `.governance/MISTAKES.md` appended by `mistakes.py record --round N --rule R "…"` in the same commit (utc stamped by the tool, never typed). `mistakes.py check <turn>` fails the turn otherwise. Session start reads MISTAKES.md before the handoff — a repeated row is a Rule-30 breach by itself.

## Rule 31 — "I edited X" is proven by a diff, or it did not happen (R86)
"عدّلت intent_gate.py" was written while the file was byte-identical to HEAD. Any sentence with an edit verb (`edited | fixed | patched | عدّلت | أصلحت | غيّرت | ضفت …`) and a file path needs an `edit_proof` block for that path in the same turn (`attest.py run -- python .governance/edit_proof.py show <path>`) whose state is not `UNCHANGED` and whose sha matches the file now. A chmod is not an edit. `edit_proof.py check <turn>` fails the turn otherwise.

## Rule 32 — A self-review that cannot say ❌ is decoration (R87)
Every self-critique block from Round 9 to Round 12 was all-✅. The block is now six fixed questions (`self_review.py`, S1-S7): attested / prechecked / skipped / pleasing / re-read / remote. ✅ on Q1/Q2 needs the sha of a block in this turn; Q4 quotes the sentence most likely written to please, verbatim from the prose; Q5 `missed:` quotes the human verbatim; Q6 ✅ needs `remote_proof: all paths match remote`. When nothing was pushed (every session without a credential), Q6 is ❌ — a review with no ❌ and no REMOTE proof fails S7.

## Rule 33 — The export is part of the chunk; a chunk that never left the sandbox was never done (R89, repeat of R39)
Round 13 attempt #1: ~40 minutes, 7 local commits, `dd8728c`, zero exports; reset; `git cat-file -t dd8728c` → "Not a valid object name". Rule 11 already said this. Now the shape is mechanical: **commit → `export_bundle.sh` → upload → URL pasted into PLAN_ROUND‑N.md in the NEXT commit.** The plan file is written before any tool work (Rule 11), and a chunk row without a URL is not ticked. `git push` is attempted only after `setup_github_environment` returns a token; on "no token" the export path is taken immediately, not after a failed push.

## Rule 34 — The turn is prechecked before it is sent, by the tools, not by the author (R88)
Seven checkers existed by Round 12; the human ran all of them, after the fact, every round. `precheck.py <turn.md> --source <human.txt>` runs intent_gate → attest → claim_check → read_proof → edit_proof → mistakes → self_review (→ req_coverage when a ledger exists) and stops at the first exit≠0. The precheck table is itself pasted as an attested block and its sha is Q2 of the self-review. A turn sent with a red precheck, or without one, is a Rule-34 breach regardless of content.

## Rule 35 — State is restored by a tool at the start of the turn and written by a tool at the end (R90)
Guide §9 promised a "compulsory silent pre-flight" that reads `Root/ai_state.json`; `grep ai_state .governance/*.py` found no tool that did, the file was 10 commits behind HEAD and `Root/PROGRESS.md` did not exist. Now the first attested block of every turn is `state_gate.py open` (prints head / state commit / drift / next_action; exit 1 on drift unless `--ack-drift`) and the last is `state_gate.py close --write` (turn_count+1, git_commit=HEAD, last_updated, next_action — rewritten by the tool, never by hand). `precheck.py` step 0 is `state_gate check`; pre-commit refuses code that moves without `ai_state.json` (`state_gate verify --staged`); CI runs `verify` and the hook negative. A turn without the two blocks fails before any other check.

## Rule 36 — A mistake made twice needs a mechanism, not a third apology (R91)
`MISTAKES.md` rows 2 and 3 were both Rule 33 and nothing noticed. `mistakes.py recurrence` counts rows per rule; any rule with ≥2 rows must have a row `--rule <n>-ESC` dated after the second occurrence that names the tool / hook / CI step which now prevents the third. Otherwise exit 1, and precheck step 6b fails the turn. The ESC row is written with `mistakes.py record` like any other row (utc from the tool). Round 14's own 33-ESC row is the export-in-the-same-command-as-the-commit rule.

## Rule 37 — An edit is proven inside its scope, and placeholder code never reaches a commit (R92, R93)
The guide documented `edit_proof.py before/after --scope A-B`; neither sub-command existed and the tool read `--numstat` only, so an edit outside the promised lines was invisible. `edit_proof.py show <file> --scope A-B` now parses `git diff -U0 HEAD` hunks in HEAD numbering (what the human read); one hunk outside [A,B] ⇒ `OUT-OF-SCOPE`, exit 1. Separately, `mock_scan.py --staged` runs in pre-commit and CI: TODO/FIXME markers, "ضع الكود هنا / your code here", `pass  # stub`, `raise NotImplementedError` outside an abstract method, lorem/placeholder literals, and a work-named function whose body is a constant return each block the commit. Opt-out is per line (`# mock-scan:allow`) and visible in the diff.

*Rules 24–26 added in Round 11, 27–29 in Round 12 (R81/R83/R84), 30–34 in Round 13 (R85–R89; designs RECONSTRUCTED after a reset destroyed the first attempt), 35–37 in Round 14 (R90–R94; C0–C4 rebuilt from the C4 export after reset #2, SHAs intact), by the Genspark consultant.*
