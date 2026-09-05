# Pending: workflow change that the sandbox token may not push

GitHub refuses pushes that modify `.github/workflows/*` from a token without the `workflows`
scope (`refusing to allow a GitHub App to create or update workflow`). So this PR carries the
new workflow **here** instead, and the live one is unchanged in this branch.

Owner applies (one command, then commit on the PR branch or after merge):

```
cp .governance/pending/governance-gate.yml .github/workflows/governance-gate.yml
git add .github/workflows/governance-gate.yml && git commit -m "ci: apply Round-6 governance-gate (fixtures, guard self-test, merge-audit job)"
```

What it adds vs. the live workflow: `--strict-done`/`--source` positive + negative fixtures,
`merge_timing_guard --self-test`, and the `merge-audit` job on `pull_request: closed` (R38).
Until applied, the new checks exist in the tree but CI does not run them.
