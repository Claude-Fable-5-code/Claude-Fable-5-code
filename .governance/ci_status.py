#!/usr/bin/env python3
"""ci_status.py — Rule 12 as a tool: print EVERY workflow run for a commit or PR, and refuse to
say "green" unless all of them are.  (R43, R50: "CI 100% green" was cited from the one push-run
that passed while 2 pull_request-runs on the same PR were red.)

Usage:
    python .governance/ci_status.py --sha <sha>            # all runs for one commit
    python .governance/ci_status.py --pr <n>               # all runs for head + merge commit of a PR
    add --json to get machine output; exit 1 if ANY run is not success (pending counts as not green).

The agent must paste this tool's output verbatim into its turn instead of writing "CI green".
Needs GITHUB_TOKEN/GH_TOKEN (or `gh auth`), and GITHUB_REPOSITORY or --repo owner/name.
"""
import json, os, subprocess, sys, urllib.request

def repo(argv):
    if "--repo" in argv: return argv[argv.index("--repo") + 1]
    if os.environ.get("GITHUB_REPOSITORY"): return os.environ["GITHUB_REPOSITORY"]
    try:
        url = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip()
        return url.split("github.com")[1].strip(":/").removesuffix(".git")
    except Exception:
        print("⛔ ci_status: cannot determine repo; pass --repo owner/name"); sys.exit(2)

def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t: return t
    try: return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception: print("⛔ ci_status: no token"); sys.exit(2)

def gh(r, path):
    req = urllib.request.Request(f"https://api.github.com/repos/{r}{path}",
        headers={"Authorization": f"Bearer {token()}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as resp: return json.load(resp)

def runs_for(r, sha):
    return gh(r, f"/actions/runs?head_sha={sha}&per_page=100").get("workflow_runs", [])

def main(argv):
    r = repo(argv); shas = []
    if "--sha" in argv: shas.append(argv[argv.index("--sha") + 1])
    if "--pr" in argv:
        pr = gh(r, f"/pulls/{argv[argv.index('--pr') + 1]}")
        shas.append(pr["head"]["sha"])
        if pr.get("merge_commit_sha") and pr.get("merged_at"): shas.append(pr["merge_commit_sha"])
    if not shas: print(__doc__); return 2
    rows = []
    for sha in dict.fromkeys(shas):
        for w in runs_for(r, sha):
            rows.append({"run_id": w["id"], "sha": sha[:7], "workflow": w["name"], "event": w["event"],
                         "status": w["status"], "conclusion": w.get("conclusion"), "url": w["html_url"]})
    red = [x for x in rows if x["conclusion"] != "success"]
    if "--json" in argv:
        print(json.dumps({"repo": r, "runs": rows, "all_green": not red and bool(rows)}, indent=1)); return 0 if rows and not red else 1
    print(f"ci_status {r}: {len(rows)} run(s) across {len(set(shas))} sha(s)")
    for x in rows:
        mark = "🟢" if x["conclusion"] == "success" else "🔴"
        print(f"  {mark} {x['run_id']} {x['sha']} {x['workflow']:<20} {x['event']:<13} {x['conclusion'] or x['status']}")
    if not rows: print("⛔ ci_status: no runs found — CI has not run; do NOT report green"); return 1
    if red: print(f"⛔ ci_status: {len(red)} of {len(rows)} runs NOT green — the word 'green' is forbidden in this turn (Rule 12)"); return 1
    print("✅ ci_status: ALL runs green"); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
