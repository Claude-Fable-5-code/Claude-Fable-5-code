#!/usr/bin/env python3
"""
merge_timing_guard.py — post-merge audit for pull requests (finding R38).

PR #3 was opened 2026-09-05T22:00:03Z and merged 22:00:07Z by its own author with zero
reviews, before the governance-gate had finished. A client-side hook cannot stop that;
a GitHub ruleset can (see .github/rulesets/), but until the owner imports it this
guard at least makes every such merge a RED run on main, visible in the Actions tab.

Fails (exit 1) when ANY of:
  - merged less than MIN_MINUTES (default 5) after the PR was opened
  - merged with zero APPROVED reviews
  - merged_by == author (self-merge)

Inputs come from env (set by the workflow from github.event.pull_request):
  PR_CREATED, PR_MERGED (ISO-8601 Z), PR_AUTHOR, PR_MERGED_BY, PR_REVIEWS_URL
Network is used only to GET PR_REVIEWS_URL (needs GITHUB_TOKEN). --self-test is offline.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MIN_MINUTES = int(os.environ.get("MIN_MINUTES", "5"))


def parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def fetch_reviews(url: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
        return json.load(r)


def evaluate(created: str, merged: str, author: str, merged_by: str, reviews: list[dict]) -> list[str]:
    problems: list[str] = []
    mins = (parse(merged) - parse(created)).total_seconds() / 60
    if mins < MIN_MINUTES:
        problems.append(f"merged {mins*60:.0f}s after opening (< {MIN_MINUTES} min) — CI cannot have been read")
    approvals = sum(1 for r in reviews if r.get("state") == "APPROVED" and r.get("user", {}).get("login") != author)
    if approvals == 0:
        problems.append("merged with zero non-author approvals")
    if author and author == merged_by:
        problems.append(f"self-merge: author == merged_by == {author}")
    return problems


def main() -> int:
    env = {k: os.environ.get(k, "") for k in ("PR_CREATED", "PR_MERGED", "PR_AUTHOR", "PR_MERGED_BY", "PR_REVIEWS_URL")}
    if not env["PR_MERGED"]:
        print("ℹ️  merge_timing_guard: PR not merged (closed without merge) — nothing to check"); return 0
    reviews = fetch_reviews(env["PR_REVIEWS_URL"]) if env["PR_REVIEWS_URL"] and env["PR_REVIEWS_URL"] != "mock" else []
    problems = evaluate(env["PR_CREATED"], env["PR_MERGED"], env["PR_AUTHOR"], env["PR_MERGED_BY"], reviews)
    if problems:
        print(f"⛔ merge_timing_guard: {len(problems)} violation(s) (R38)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("✅ merge_timing_guard: merge timing, approvals and merger OK"); return 0


def self_test() -> int:
    """Offline. PR #3's real data must fail on all three counts; a healthy PR must pass."""
    bad = evaluate("2026-09-05T22:00:03Z", "2026-09-05T22:00:07Z", "Claude-Fable-5-code", "Claude-Fable-5-code", [])
    if len(bad) != 3:
        print(f"❌ self-test: PR #3 pattern produced {len(bad)} violations, expected 3: {bad}"); return 1
    good = evaluate("2026-09-05T22:00:00Z", "2026-09-05T22:15:00Z", "agent", "owner",
                    [{"state": "APPROVED", "user": {"login": "owner"}}])
    if good:
        print(f"❌ self-test: healthy PR flagged: {good}"); return 1
    print("✅ merge_timing_guard self-test ok (PR #3 pattern → 3 violations; healthy PR → 0)"); return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv else main())
