#!/usr/bin/env python3
"""
remote_proof.py — a file "exists" only if it exists on the REMOTE (R57, Round 9).

Usage:
    python .governance/remote_proof.py <path> [<path> ...] [--ref main] [--repo owner/name]

For each path, fetches the blob from GitHub (anonymous works on public repos) and
compares its sha256 with the local working-tree file. Prints one line per path:

    ✅ REMOTE  <path>  sha=<12>            local == remote @ <ref>
    🟡 DIFFERS <path>  local=<12> remote=<12>   (committed locally, not pushed / stale)
    🔴 MISSING <path>  local exists, NOT on remote  ← "updated" claims about this file are false
    ⚫ ABSENT  <path>  neither local nor remote

Exit 1 if any path is DIFFERS / MISSING / ABSENT.

Why this exists: the agent wrote "✅ memory log updated (ai_state.json, CHANGELOG_DECISIONS.md,
PROGRESS.md, ANCHORS.md)" in Round 8. On the remote, ai_state.json was last touched two rounds
earlier and CHANGELOG_DECISIONS.md never existed. Everything it "remembered" lived on a machine
that is reset every few minutes. The agent must paste this tool's output after any sentence that
says a file was created, updated, saved, sealed, or anchored (Rule 18).
"""
import hashlib, json, os, subprocess, sys, urllib.request, urllib.error


def repo_from_origin():
    try:
        url = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True, stderr=subprocess.DEVNULL).strip()
        url = url[:-4] if url.endswith(".git") else url
        return "/".join(url.replace(":", "/").split("/")[-2:])
    except Exception:
        return os.environ.get("GITHUB_REPOSITORY")


def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t:
        return t
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def remote_blob(repo, path, ref):
    h = {"Accept": "application/vnd.github.raw+json"}
    t = token()
    if t:
        h["Authorization"] = f"Bearer {t}"
    url = f"https://api.github.com/repos/{repo}/contents/{urllib.request.quote(path)}?ref={ref}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main(argv):
    def opt(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default
    ref = opt("--ref", "main")
    repo = opt("--repo", None) or repo_from_origin()
    paths = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in ("--ref", "--repo"))]
    if not repo or not paths:
        print(__doc__)
        return 2
    bad = 0
    print(f"remote_proof {repo}@{ref}: {len(paths)} path(s)")
    for p in paths:
        local = open(p, "rb").read() if os.path.isfile(p) else None
        remote = remote_blob(repo, p, ref)
        if local is None and remote is None:
            print(f"  ⚫ ABSENT  {p}  neither local nor remote"); bad += 1
        elif remote is None:
            print(f"  🔴 MISSING {p}  local exists, NOT on remote  ← any 'updated/saved' claim about this file is false"); bad += 1
        elif local is None:
            print(f"  🟡 REMOTE-ONLY {p}  remote={sha(remote)[:12]} (not in this checkout)")
        elif sha(local) != sha(remote):
            print(f"  🟡 DIFFERS {p}  local={sha(local)[:12]} remote={sha(remote)[:12]}  (not pushed / stale)"); bad += 1
        else:
            print(f"  ✅ REMOTE  {p}  sha={sha(local)[:12]}")
    if bad:
        print(f"⛔ remote_proof: {bad} of {len(paths)} path(s) not proven on remote — do not write 'updated' about them (Rule 18)")
        return 1
    print("✅ remote_proof: all paths match remote")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
