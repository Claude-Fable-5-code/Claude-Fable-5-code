# pending/ — workflow changes the sandbox token cannot push
Round 7: `governance-gate.yml` adds `--coverage-min 85` (R47) to both req_coverage steps.
Apply:
    cp .governance/pending/governance-gate.yml .github/workflows/governance-gate.yml && git add -A && git commit -m "ci: R47 coverage-min" 
Then open a PR and **wait ≥ 5 min + 1 approval** before merging (Rule 10). PR #5 was merged in 3 s and `merge-audit` went RED — do not repeat.

## Round 8 — R52 fix (owner applies; sandbox token lacks `workflows` scope)
`cp .governance/pending/governance-gate.yml .github/workflows/governance-gate.yml`
One-line diff: `HEAD:main` → `HEAD:refs/heads/main` in the pre-push behavioural test. Without it `gate`
is red on every `pull_request` event and the ruleset's required check `gate` will block every PR.

## Round 12 — checker-family CI step (owner applies if the sandbox push to `.github/workflows` is rejected)
`cp .governance/pending/governance-gate.yml .github/workflows/governance-gate.yml`
Adds the "checker family self-tests" step: self-tests for intent_gate / claim_check / read_proof plus three negatives
from the real Round-12 gist (R81 typed verdict → C7, R83 CONFIRM-FIRST without mirror, R84 diagnosis without read_proof).
