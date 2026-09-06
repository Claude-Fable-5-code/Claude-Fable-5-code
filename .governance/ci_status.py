#!/usr/bin/env python3
"""ci_status.py — Rule 12 as a tool: print EVERY workflow run for a commit or PR, and refuse to
say "green" unless all of them are.  (R43, R50: "CI 100% green" was cited from the one push-run
that passed while 2 pull_request-runs on the same PR were red.)

Usage:
    python .governance/ci_status.py --sha <sha>            # all runs for one commit (+ its PR head if it is a merge)
    python .governance/ci_status.py --pr <n>               # all runs for head + merge commit of a PR
    python .governance/ci_status.py --self-test            # offline; the R100 blind spot must be caught
    add --json to get machine output; exit 1 if ANY run is not success (pending counts as not green).

The agent must paste this tool's output verbatim into its turn instead of writing "CI green".
Needs GITHUB_TOKEN/GH_TOKEN (or `gh auth`), and GITHUB_REPOSITORY or --repo owner/name.

Round 16 (R100). PR #15 was self-merged with zero reviews; the `merge-audit` job failed (run
34057701060) — but that run is attributed to the PR HEAD sha under the `pull_request:closed`
event, not to the merge commit. `--sha <merge sha>` therefore printed "ALL runs green" for `main`,
and `--pr 15` run BEFORE the merge could not see a run that only exists AFTER it. Two fixes:
  * `--sha` on a commit that GitHub maps to a merged PR (`/commits/{sha}/pulls`) also pulls the
    PR head sha's runs, so the post-merge audit is in the same block as main's push run.
  * `--pr` on a MERGED PR demands at least one `pull_request` run created at/after `merged_at`
    (that is the merge-audit run). None yet ⇒ "⏳ merge-audit run not found" ⇒ exit 1, not green.
"""
import json, os, subprocess, sys, urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def repo(argv):
    if "--repo" in argv: return argv[argv.index("--repo") + 1]
    if os.environ.get("GITHUB_REPOSITORY"): return os.environ["GITHUB_REPOSITORY"]
    try:
        url = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True, encoding="utf-8", errors="replace").strip()
        return url.split("github.com")[1].strip(":/").removesuffix(".git")
    except Exception:
        print("⛔ ci_status: cannot determine repo; pass --repo owner/name"); sys.exit(2)

def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t: return t
    try: return subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception: return None  # public repos: anonymous API works (60 req/h) — R56

def gh(r, path):
    h = {"Accept": "application/vnd.github+json"}
    t = token()
    if t: h["Authorization"] = f"Bearer {t}"
    req = urllib.request.Request(f"https://api.github.com/repos/{r}{path}", headers=h)
    with urllib.request.urlopen(req, timeout=30) as resp: return json.load(resp)

def runs_for(r, sha):
    return gh(r, f"/actions/runs?head_sha={sha}&per_page=100").get("workflow_runs", [])

def full_sha(r, sha):
    """`/actions/runs?head_sha=` silently matches nothing for an abbreviated sha — expand it first (R100)."""
    if len(sha) == 40: return sha
    try: return gh(r, f"/commits/{sha}")["sha"]
    except Exception: return sha

def merged_pr_for_sha(r, sha):
    """The merged PR whose merge_commit_sha is `sha`, or None. Ordinary commits return None."""
    try:
        for p in gh(r, f"/commits/{sha}/pulls"):
            if p.get("merged_at") and (p.get("merge_commit_sha") or "").startswith(sha[:7]):
                return p
    except Exception:
        pass
    return None

def collect(shas, runs_for_fn):
    rows = []
    for sha in dict.fromkeys(shas):
        for w in runs_for_fn(sha):
            rows.append({"run_id": w["id"], "sha": sha[:7], "workflow": w["name"], "event": w["event"],
                         "status": w["status"], "conclusion": w.get("conclusion"), "url": w.get("html_url", ""),
                         "created_at": w.get("created_at", "")})
    return rows

def evaluate(rows, merged_pr):
    """Return (red_rows, problems). merged_pr = {"merged_at": iso, "head_sha": sha} or None (R100)."""
    red = [x for x in rows if x["conclusion"] != "success"]
    problems = []
    if not rows:
        problems.append("no runs found — CI has not run; do NOT report green")
    if merged_pr:
        head = merged_pr["head_sha"][:7]
        audit = [x for x in rows if x["sha"] == head and x["event"] == "pull_request"
                 and x["created_at"] >= merged_pr["merged_at"]]
        if not audit:
            problems.append(f"PR merged at {merged_pr['merged_at']} but no pull_request run on head {head} "
                            f"created at/after that time — the merge-audit run is missing or not yet started (R100); NOT green")
    return red, problems

def main(argv):
    if "--self-test" in argv: return self_test()
    r = repo(argv); shas = []; merged = None
    if "--sha" in argv:
        sha = full_sha(r, argv[argv.index("--sha") + 1]); shas.append(sha)
        pr = merged_pr_for_sha(r, sha)
        if pr:
            shas.append(pr["head"]["sha"]); merged = {"merged_at": pr["merged_at"], "head_sha": pr["head"]["sha"], "number": pr["number"]}
    if "--pr" in argv:
        pr = gh(r, f"/pulls/{argv[argv.index('--pr') + 1]}")
        shas.append(pr["head"]["sha"])
        if pr.get("merge_commit_sha") and pr.get("merged_at"):
            shas.append(pr["merge_commit_sha"]); merged = {"merged_at": pr["merged_at"], "head_sha": pr["head"]["sha"], "number": pr["number"]}
    if not shas: print(__doc__); return 2
    rows = collect(shas, lambda s: runs_for(r, s))
    red, problems = evaluate(rows, merged)
    ok = rows and not red and not problems
    if "--json" in argv:
        print(json.dumps({"repo": r, "runs": rows, "problems": problems, "all_green": bool(ok)}, indent=1)); return 0 if ok else 1
    note = f" (merged PR #{merged['number']} — head-sha runs included)" if merged else ""
    print(f"ci_status {r}: {len(rows)} run(s) across {len(set(shas))} sha(s){note}")
    for x in rows:
        mark = "🟢" if x["conclusion"] == "success" else "🔴"
        print(f"  {mark} {x['run_id']} {x['sha']} {x['workflow']:<20} {x['event']:<13} {x['conclusion'] or x['status']}")
    for p in problems: print(f"⏳ ci_status: {p}")
    if not rows: return 1
    if red: print(f"⛔ ci_status: {len(red)} of {len(rows)} runs NOT green — the word 'green' is forbidden in this turn (Rule 12)"); return 1
    if problems: print("⛔ ci_status: verdict withheld — the word 'green' is forbidden in this turn (Rule 12/16)"); return 1
    print("✅ ci_status: ALL runs green"); return 0

def self_test():
    """Offline. Replays PR #15 (R100): the merge commit's own runs are green, the merge-audit failure lives on the head sha."""
    MERGE, HEAD = "cd7a215ca931040c20aa6b1fe38fcacffdd2d160", "c52f5f53fc29e856bd2e68fbba7aba4430cc8271"
    fake = {
        MERGE: [{"id": 34057701138, "name": "governance-gate", "event": "push", "status": "completed", "conclusion": "success", "created_at": "2026-09-06T20:20:48Z"}],
        HEAD:  [{"id": 34057701060, "name": "governance-gate", "event": "pull_request", "status": "completed", "conclusion": "failure", "created_at": "2026-09-06T20:20:49Z"},
                {"id": 34057350034, "name": "governance-gate", "event": "pull_request", "status": "completed", "conclusion": "success", "created_at": "2026-09-06T20:14:08Z"},
                {"id": 34057300947, "name": "governance-gate", "event": "push", "status": "completed", "conclusion": "success", "created_at": "2026-09-06T20:13:13Z"}],
    }
    pr = {"merged_at": "2026-09-06T20:20:47Z", "head_sha": HEAD}
    ok = True
    # 1) OLD behaviour: merge sha alone → green. That is the blind spot; evaluate() with no PR context must still say green (nothing to know).
    red, prob = evaluate(collect([MERGE], fake.get), None); ok &= not red and not prob
    # 2) NEW: merge sha + PR head → the failure is visible → red
    red, prob = evaluate(collect([MERGE, HEAD], fake.get), pr); ok &= len(red) == 1 and red[0]["run_id"] == 34057701060
    # 3) --pr run BEFORE the merge (audit run absent) on a merged PR → problem, not green
    before = {HEAD: fake[HEAD][1:], MERGE: fake[MERGE]}
    red, prob = evaluate(collect([HEAD, MERGE], before.get), pr); ok &= not red and len(prob) == 1 and "merge-audit" in prob[0]
    # 4) healthy merged PR: audit run present and success → green
    healthy = {HEAD: [dict(fake[HEAD][0], conclusion="success")] + fake[HEAD][1:], MERGE: fake[MERGE]}
    red, prob = evaluate(collect([HEAD, MERGE], healthy.get), pr); ok &= not red and not prob
    # 5) no runs at all → problem
    red, prob = evaluate(collect([HEAD], (lambda s: [])), None); ok &= len(prob) == 1 and "no runs" in prob[0]
    # 6) a pending run counts as not green
    pend = {HEAD: [dict(fake[HEAD][0], status="in_progress", conclusion=None)]}
    red, prob = evaluate(collect([HEAD], pend.get), None); ok &= len(red) == 1
    print(("✅" if ok else "❌") + " ci_status self-test " + ("ok (6 cases: R100 merge-sha blind spot, pre-merge --pr, healthy, empty, pending)" if ok else "FAILED"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
