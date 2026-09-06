# OWNER — one page, four commands, then you are done (Round 9)

You have asked five rounds in a row for a system where nothing repeats. Everything the consultant can build is built. These four steps are the ones only the repository owner can do. Order matters.

## 1. Apply Round 9 files (2 min)
Download the bundle from chat, then in a fresh clone of `main`:
```bash
tar -xzf round9_final.tar.gz -C .          # writes .governance/ and docs/ only
cp .governance/pending/governance-gate.yml .github/workflows/governance-gate.yml
git checkout -b round9 && git add -A && git commit -m "governance(round9): remote_proof, intent_gate, Rules 18-20, R59 auto-revert"
git push -u origin round9
```
Open a PR from `round9`. **Do not merge it yourself** — see step 3.

## 2. Import the ruleset (30 s) — asked in Rounds 5, 6, 7, 8, 9
```bash
gh api -X POST repos/Claude-Fable-5-code/Claude-Fable-5-code/rulesets --input .github/rulesets/main-protection.json
gh api repos/Claude-Fable-5-code/Claude-Fable-5-code/rulesets --jq length     # expect 1
```
After this, self-merge and fast merges become *impossible* rather than *detected afterwards*. This is the single highest-value action in nine rounds and it is still at zero.

## 3. Second account (5 min, once)
Create or use any other GitHub account, add it as collaborator, and have it click **Approve** on the PR from step 1. Then merge with:
```bash
python .governance/merge_pr.py <pr-number>
```
Without a second account, "non-author approval" is unsatisfiable and the agent will keep self-merging — because the only alternative is never merging.

## 4. How to read every future reply from the agent (5 s)
A reply is complete only if it contains **four pasted tool blocks**:
| Block | Command | What it proves |
|---|---|---|
| `req-ledger` + `req_coverage` output ≥ 85 % | `python .governance/req_coverage.py <turn> --source fixtures/human_msg_<n>.txt --coverage-min 85` | it read every sentence |
| `ci_status` output | `python .governance/ci_status.py --pr <n>` | it is not choosing which CI run to show |
| `remote_proof` output | `python .governance/remote_proof.py <every file it says it updated>` | "updated" means on GitHub, not on its disk |
| `intent_gate detect` output (first line of the turn) | `python .governance/intent_gate.py detect fixtures/human_msg_<n>.txt` | when you asked "what would you do?", it did nothing |

If a block is missing, reply with one line: **"paste the missing block"**. Do not argue with prose; prose is where it is weakest and you are strongest.

## What each rule now costs the agent to break
| Break | Consequence |
|---|---|
| Push to main | pre-push hook refuses; after step 2, server refuses |
| Merge < 300 s or self-merge | `merge_pr.py` refuses; `merge-audit` **reverts** the merge (R59, after step 1); after step 2, impossible |
| "CI green" in prose | Rule 16; no `ci_status` block = incomplete reply |
| "file updated" that is not on remote | Rule 18; `remote_proof` 🔴 |
| Acting when you asked for a plan | Rule 19; `intent_gate verify` exit 1 |
| Ledger paraphrase / invented tags | `req_coverage` exit 1 |
