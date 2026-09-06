#!/usr/bin/env python3
"""merge_pr.py — the ONLY sanctioned way for an agent/script to merge a PR (Rule 10, R46).

PR #3 (4 s) and PR #5 (3 s) were self-merged by a helper script that called the merge API
right after opening. `merge-audit` in CI can only turn main RED afterwards; this script
refuses BEFORE. It is a client-side guard — the server-side fix is still the owner importing
.github/rulesets/main-protection.json. Until then, push_to_github.py MUST call this instead
of the merge endpoint.

    python .governance/merge_pr.py <pr_number> [--min-age 300] [--min-reviews 1] [--dry-run]

Refuses (exit 1) when ANY holds:
  * PR age < --min-age seconds               (default 300)
  * approving reviews < --min-reviews         (default 1)
  * author == the token's login and reviews from others == 0
  * any check-run on the head SHA is not 'success' (pending counts as not green)
Requires GITHUB_TOKEN / GH_TOKEN with repo scope. Never prints the token.
"""
from __future__ import annotations
import json, os, sys, urllib.request, datetime as dt

REPO = os.environ.get("GITHUB_REPOSITORY", "Claude-Fable-5-code/Claude-Fable-5-code")
API = f"https://api.github.com/repos/{REPO}"

def gh(path: str, method: str = "GET", body: dict | None = None):
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not tok:
        print("⛔ merge_pr: GITHUB_TOKEN/GH_TOKEN not set"); sys.exit(2)
    req = urllib.request.Request(API + path, method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def main(argv: list[str]) -> int:
    nums = [a for a in argv[1:] if a.isdigit()]
    if not nums: print(__doc__); return 2
    n = int(nums[0])
    def opt(name, default):
        return int(argv[argv.index(name) + 1]) if name in argv else default
    min_age, min_rev, dry = opt("--min-age", 300), opt("--min-reviews", 1), "--dry-run" in argv

    try:
        me = json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/user",
              headers={"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')}"})))["login"]
    except Exception:
        me = None
    pr = gh(f"/pulls/{n}")
    if pr["state"] != "open": print(f"⛔ merge_pr: PR #{n} is {pr['state']}"); return 1
    created = dt.datetime.fromisoformat(pr["created_at"].rstrip("Z")).replace(tzinfo=dt.timezone.utc)
    age = (dt.datetime.now(dt.timezone.utc) - created).total_seconds()
    reviews = gh(f"/pulls/{n}/reviews")
    approvals = {r["user"]["login"] for r in reviews if r["state"] == "APPROVED" and r["user"]["login"] != pr["user"]["login"]}
    checks = gh(f"/commits/{pr['head']['sha']}/check-runs").get("check_runs", [])
    not_green = [c["name"] for c in checks if c.get("conclusion") != "success"]

    problems = []
    if age < min_age: problems.append(f"PR age {age:.0f}s < {min_age}s (R38: PR #3 = 4 s, PR #5 = 3 s)")
    if len(approvals) < min_rev: problems.append(f"approvals from non-authors = {len(approvals)} < {min_rev}")
    if me and pr["user"]["login"] == me and not approvals: problems.append(f"self-merge by author '{me}' with zero external reviews")
    if not checks: problems.append("no check-runs on head SHA yet — CI has not even started")
    if not_green: problems.append(f"checks not green: {not_green}")

    print(f"PR #{n} '{pr['title'][:60]}' age={age:.0f}s approvals={sorted(approvals)} checks={len(checks)} not_green={len(not_green)}")
    if problems:
        print("⛔ merge_pr: REFUSED"); [print("  -", p) for p in problems]; return 1
    if dry: print("✅ merge_pr: would merge (dry-run)"); return 0
    res = gh(f"/pulls/{n}/merge", "PUT", {"merge_method": "merge"})
    print(f"✅ merge_pr: merged {res.get('sha','')[:7]} — https://github.com/{REPO}/pull/{n}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
