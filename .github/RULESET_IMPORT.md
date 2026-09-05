# How to activate branch protection (owner only — 2 minutes)

The file `rulesets/main-protection.json` is an importable GitHub **Repository Ruleset**.
Until it is imported, `main` accepts direct pushes (verified via API: `"protected": false` on 2026-09-05).

1. Repo → **Settings** → **Rules** → **Rulesets**
2. **New ruleset** ▾ → **Import a ruleset**
3. Upload `.github/rulesets/main-protection.json`
4. Confirm **Enforcement status = Active** → **Create**

What it enforces (nothing an agent can turn off):
| Rule | Effect |
|---|---|
| `pull_request` (1 approval, code-owner review, last-push approval) | No commit reaches `main` without a human clicking Approve **after** the last push |
| `required_status_checks: gate` | The `governance-gate` workflow job (`gate`) must be green |
| `non_fast_forward` + `deletion` | No force-push, no branch deletion |
| `required_linear_history` | No merge commits sneaking in un-reviewed history |
| `bypass_actors: []` | **Nobody** bypasses — including the owner. Change this consciously if needed. |

Also enable (same Settings page → **Code security**):
- **Secret scanning** → On
- **Push protection** → On  (blocks a push server-side the moment a token pattern is detected)
