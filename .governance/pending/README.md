# pending/ — workflow changes the sandbox token cannot push
Round 7: `governance-gate.yml` adds `--coverage-min 85` (R47) to both req_coverage steps.
Apply:
    cp .governance/pending/governance-gate.yml .github/workflows/governance-gate.yml && git add -A && git commit -m "ci: R47 coverage-min" 
Then open a PR and **wait ≥ 5 min + 1 approval** before merging (Rule 10). PR #5 was merged in 3 s and `merge-audit` went RED — do not repeat.
