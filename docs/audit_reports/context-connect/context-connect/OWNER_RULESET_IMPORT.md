# Import the main-protection ruleset — 1 command, owner only (4th round asking)

Every self-merge (PR #3 4 s, PR #5 3 s, PR #6 0 reviews) was possible because `main` has **0 rulesets**
(verified `GET /repos/…/rulesets` → `[]` on 2026-09-06). The sandbox tokens (Elric412, mehmetcihattapu)
get `403 Resource not accessible by integration` on POST — only the repo owner can do this.

## Option A — one command (owner's machine, `gh auth login` as Claude-Fable-5-code)
```bash
gh api -X POST repos/Claude-Fable-5-code/Claude-Fable-5-code/rulesets \
  --input .github/rulesets/main-protection.json
```
Expect HTTP 201 and a JSON with `"id"`. Verify: `gh api repos/Claude-Fable-5-code/Claude-Fable-5-code/rulesets --jq 'length'` → `1`.

## Option B — 3 clicks
Settings → Rules → Rulesets → **New ruleset ▾ → Import a ruleset** → pick `.github/rulesets/main-protection.json` → Create.

## What it enforces (from the file)
- `main`: no deletion, no force-push, linear history
- PR required with **1 approving review from a non-author**, stale approvals dismissed on push,
  last push must be approved, threads resolved, **CODEOWNERS review** (`.github/CODEOWNERS` exists)
- required status check **`gate`** must be green on the PR head (strict = branch up to date)

## Consequence
`push_to_github.py`, `merge_pr.py`, the agent, and the owner **all** become unable to merge without a
second human's approval and a green `gate`. This is the only fence that does not depend on the agent
choosing to obey. Every rule 10–17 is a request; this is a lock.

## Note on `gate` being red on every PR (R52)
Until commit in this round, `gate` failed on **every** `pull_request` event (PR #5, PR #6) because the
behavioural test used `HEAD:main` in a detached checkout. With the ruleset active this would have
**blocked** those merges — which is exactly why it should have been imported first. Fixed to
`HEAD:refs/heads/main`; verified in a detached-HEAD simulation locally (Rule 7 + Rule 8 both trigger).
