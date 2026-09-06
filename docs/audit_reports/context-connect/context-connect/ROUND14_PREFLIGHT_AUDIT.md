# Round 14 — Preflight forensic audit of `USER_COMPLETE_OPERATING_GUIDE.md` (delivered 2026‑09‑06, before reset #1)

Scope: the guide committed at `463a967` (235 lines, read in full via `read_proof index`,
`ATTEST tool=read_proof sha256=5503f36ff1127ece head=463a967 exit=0`). Every row below is a command that was run
in `/home/user/webapp`; no row is opinion. The turn itself was not prechecked (no turn.md existed before send) —
that gap is what C1/C2 of this round close.

## 1. Mechanical verification table

| check | actual output |
|---|---|
| `git status --short \| wc -l` / branch | `0` / `main` |
| `git log -1` | `463a967 Create USER_COMPLETE_OPERATING_GUIDE.md` (parent `b4b6fa9 Merge PR #13`) |
| `git diff --stat b4b6fa9..HEAD` | one file: `USER_COMPLETE_OPERATING_GUIDE.md` +235 |
| 7 tool SHAs vs tree of `b4b6fa9` | 7/7 identical (precheck 6d73d51ee8b3 · mistakes a2760d687a33 · edit_proof d05409eca1b9 · self_review 4f4bca0bbdf4 · read_proof 902249eb43f2 · intent_gate 19d39238671f · claim_check 2e68914830a8) |
| 7 × `--self-test` | 7/7 exit 0 |
| `attest.py run -- precheck.py` (as written in the prompt) | `exit=2` — usage; precheck needs `<turn.md> --source <msg>`; the prompt's command is missing two arguments, not a tool fault |
| `Root/ai_state.json` | `git_commit: e9d0bbe`, `current_tag: [ROUND10-INTEGRATED-LOCAL]`, `turn_count: 297` → `git log e9d0bbe..HEAD \| wc -l` = **10** commits behind |
| `ls Root/PROGRESS.md CHANGELOG_DECISIONS.md push_to_github.bat` | all three: No such file (only `proposed_files/PROGRESS.md` exists) |
| `grep -c "mistake-ack" mistakes.py intent_gate.py AGENT_HARD_RULES.md` | 0 / 0 / 0 |
| `grep -rl ai_state .governance/*.py` | claim_check.py (regex C5 only), probe_init_root.py, remote_proof.py — no gate |
| `grep -lE "precheck\|self_review\|read_proof\|ai_state" .governance/hooks/*` | none (hooks run secret_scan + path_scan only) |
| `grep -nEi "length\|lazy\|summary" self_review.py` | 0 matches — the tool does not measure brevity |
| `edit_proof.py` sub‑commands | `show`, `check`, `--self-test` only; `show_one` computes `git diff --numstat`, state ∈ {UNTRACKED, MODIFIED, STAGED, COMMITTED-IN-HEAD, UNCHANGED} — no line‑range logic |
| `mistakes.py` sub‑commands | `record --round N --rule R "…"`, `check <turn.md>`, `--self-test` — no `add` |
| Rule numbering (AGENT_HARD_RULES.md L209‑230) | 27 CONFIRM‑FIRST · 28 read‑proof · 29 checker verdict · **30 admitted mistake = ledger row** · **31 edit proven by diff** · 32 self‑review · **33 export per chunk** · 34 precheck |

## 2. Chapter‑by‑chapter refutation

| § | verdict | proven gap (guide line) | fix (chunk) |
|---|---|---|---|
| 1 Emergencies (L21‑45) | weak | L33 `Stop-Process -Name python -Force` kills **all** python. L38 points at `Root/PROGRESS.md` which does not exist. Restoring from `ai_state.json` restores a state 10 commits old | kill by PID; create PROGRESS.md; `state_gate` refuses `git_commit ≠ HEAD` (C1/C2/C6) |
| 2 Anti‑hallucination (L52‑63) | misleading | L58 ````mistake-ack` block: 0 matches in any tool/rule. L62 `mistakes.py add`: real verb is `record`. L52 "Rule 31": real is Rule 30. Ledger records after the fact; **no recurrence guard** | fix names; `mistakes.py check --recurrence` (C4/C6) |
| 3 No‑guessing (L75‑90) | **false claim** | L88‑89 `edit_proof.py before/after --scope 40-50`: sub‑commands do not exist. L90 "breaks the code and refuses": it fails a text check on the turn, nothing more. L86 "Rule 31/33": 33 is export | real `--scope A-B` from diff hunks (C5); text fix (C6) |
| 4 HAR / mock (L94‑118) | no tool | zero checkers for TODO/placeholder/mock in `.governance/` | `mock_scan.py` in pre‑commit + CI (C5) |
| 5 Laziness (L122‑139) | partial | self_review checks Q1‑Q6 + evidence only; does not measure brevity. L139 "prevents the reply": nothing blocks sending | accept the limit; brevity is caught by claim_check (prose without block) + req_coverage |
| 6 Push & merge (L143‑163) | **governance regression** | `push_to_github.bat` not in repo. L157‑158 auto‑merge after 300 s contradicts Rule 20 ("floor, not target") and Rules 10/13 (no self‑merge) | remove auto‑merge from guide; merge is manual after `ci_status.py` green (C6) |
| 7 Tri‑party loop (L167‑189) | acceptable | L186 "merge into main" = same self‑merge path | same fix (C6) |
| 8 Magic prompts (L192‑205) | acceptable | L203 → missing file; L198 → wrong verb | fix after C5 (C6) |
| 9 Compulsory self‑recall (L211‑224) | **zero enforcement** | L217 "the system forces it to read ai_state": no hook, no precheck step, no CI step requires reading at start or updating at end. Prose only | §3 below (C1‑C3) |

## 3. Enforcement architecture (what CAN be enforced, honestly)

No hook in any repo or IDE intercepts "send chat reply". What can be enforced is that a reply which did not
restore/update state is **machine‑detectable and rejected** by four independent gates:

```
state_gate.py  (new, Round 14 — R90)
  open            reads Root/ai_state.json + Root/PROGRESS.md; prints a `state-open` block:
                  head, ai_state.git_commit, drift=N commits, next_action
                  → exit 1 when drift>0 unless --ack-drift (forces awareness of the gap)
  close [--write] verifies ai_state changed since open: turn_count+1, git_commit==HEAD,
                  last_updated>open.utc, next_action non-empty; prints `state-close`;
                  --write performs the update itself (human decision, fixture line 3)
  check <turn.md> exit 1 unless: first ATTEST block in the turn = state_gate open,
                  last ATTEST block = state_gate close, same head in both
  verify          repo-level: ai_state.git_commit ∈ last 2 commits, PROGRESS.md exists
```
- **precheck.py**: step 0 = `state_gate check`. Without it the turn fails precheck → self_review Q2 cannot cite a passing sha.
- **pre‑commit hook**: staged files other than `Root/ai_state.json` ⇒ `ai_state.json` must be staged and `state_gate verify --staged` exit 0 ("state moves with code").
- **CI `governance-gate.yml`**: `state_gate.py verify` + `--self-test`.
- **self_review**: Q7 `state:` cites the sha of the `state-close` block.

## 4. Round 14 chunk plan
See `PLAN_ROUND14.md` (authoritative; ticks + URLs live there).

## 5. Self‑review of the audit turn (as sent, before reset #1)
```
Q1 attested: ✅ precheck (a3cf397d57d47887) and read_proof (5503f36ff1127ece) blocks carried ATTEST head=463a967; git/grep output pasted verbatim.
Q2 prechecked: ❌ precheck was not run on the turn (no turn.md exported before send) — the very gap C1 closes.
Q3 skipped: ci_status.py — no GITHUB_TOKEN in the sandbox.
Q4 pleasing: ❌ §9 rated "zero enforcement" despite being written with high confidence; not softened.
Q5 re-read: ✅ the prompt's four tasks (discovery / refutation / compulsory recall / plan) all answered; the prompt's own precheck command is missing two arguments and was reported.
Q6 remote: ✅ origin/main = 463a967 via git fetch; no push claimed.
```
