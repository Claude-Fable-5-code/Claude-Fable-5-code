#!/usr/bin/env python3
"""
secret_scan.py — portable secret scanner (R16 / R19).

Usage:
  python .governance/secret_scan.py                 # scan working tree (tracked files)
  python .governance/secret_scan.py --staged        # scan staged diff (pre-commit)
  python .governance/secret_scan.py --range A..B    # scan commits about to be pushed (pre-push)
  python .governance/secret_scan.py --files f1 f2   # scan explicit files

Exit 0 = clean. Exit 1 = at least one hit. Exit 2 = usage/runtime error.
No network, no dependencies, no hard-coded paths. Works on Windows/Linux/macOS.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Each pattern: (name, compiled regex). Keep them tight to avoid false positives.
PATTERNS = [
    ("github_classic_pat", re.compile(r"\bghp_[A-Za-z0-9]{36}\b")),
    ("github_fine_grained_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("github_oauth", re.compile(r"\bgho_[A-Za-z0-9]{36}\b")),
    ("github_app", re.compile(r"\b(ghu|ghs|ghr)_[A-Za-z0-9]{36}\b")),
    ("openai_key", re.compile(r"\bsk-(proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("anthropic_key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("slack_token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("private_key_block", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("url_with_credentials", re.compile(r"https?://[^/\s:@]+:[^/\s@]+@[^/\s]+")),
    ("url_with_token_user", re.compile(r"https?://(x-access-token|oauth2|ghp_[A-Za-z0-9]+)[:@][^\s]+@")),
    ("generic_assignment", re.compile(
        r"(?i)\b(api[_-]?key|secret|token|passwd|password)\b\s*[:=]\s*['\"][A-Za-z0-9_\-/.+=]{16,}['\"]")),
    # Round 5 (R21/R22): shapes seen in the leaked transcript.
    ("credential_helper_output", re.compile(r"(?i)^\s*(print\(\s*)?['\"]?password=(gh[pousr]_|github_pat_|sk-|AKIA)")),
    ("bearer_header_literal", re.compile(r"(?i)authorization['\"]?\s*[:=]\s*['\"]?(bearer|token)\s+(gh[pousr]_|github_pat_|sk-|AKIA)[A-Za-z0-9_\-]{10,}")),
    # '!' must be followed by a command token (letter, slash, backslash) — prose like "=!…" does not match.
    ("inline_credential_helper", re.compile(r"credential\.helper\s*=\s*['\"]?![A-Za-z/\\]")),
    ("cmdkey_with_pass", re.compile(r"(?i)cmdkey\s+/generic:[^\s]+\s+/user:[^\s]+\s+/pass:\S{8,}")),
]

# Files we never scan (binary / vendored / this scanner's own docs).
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".tar", ".woff", ".woff2", ".ttf"}
SKIP_PARTS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
# Documentation that intentionally quotes *redacted* examples.
ALLOW_MARKER = "secret-scan:allow"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def _iter_lines_from_text(text: str, label: str):
    for i, line in enumerate(text.splitlines(), 1):
        yield label, i, line


def scan_text(label: str, text: str) -> list[tuple[str, int, str, str]]:
    hits = []
    for lbl, ln, line in _iter_lines_from_text(text, label):
        if ALLOW_MARKER in line:
            continue
        for name, rx in PATTERNS:
            if rx.search(line):
                hits.append((lbl, ln, name, _redact(line)))
                break
    return hits


def _redact(line: str) -> str:
    """Never print the secret itself — show the shape only."""
    def mask(m: re.Match) -> str:
        s = m.group(0)
        return s[:6] + "…" + s[-3:] if len(s) > 12 else "…"
    out = line.strip()
    for _, rx in PATTERNS:
        out = rx.sub(mask, out)
    return out[:160]


def files_from_tree() -> list[Path]:
    out = _git("ls-files", "-z")
    return [Path(p) for p in out.split("\0") if p]


def files_from_staged() -> list[Path]:
    out = _git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    return [Path(p) for p in out.split("\0") if p]


def scan_files(paths: list[Path]) -> list[tuple[str, int, str, str]]:
    hits = []
    for p in paths:
        if p.suffix.lower() in SKIP_SUFFIXES or any(part in SKIP_PARTS for part in p.parts):
            continue
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hits.extend(scan_text(str(p), text))
    return hits


def scan_range(rng: str) -> list[tuple[str, int, str, str]]:
    """Scan added lines in every commit of the range (pre-push)."""
    diff = _git("log", "-p", "--no-color", "--format=commit %h", rng)
    hits = []
    current = "?"
    for i, line in enumerate(diff.splitlines(), 1):
        if line.startswith("commit "):
            current = line.split()[1]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if ALLOW_MARKER in line:
            continue
        for name, rx in PATTERNS:
            if rx.search(line):
                hits.append((f"commit {current}", i, name, _redact(line[1:])))
                break
    return hits


def scan_remote_urls() -> list[tuple[str, int, str, str]]:
    """A remote URL that embeds credentials is itself a leak (R16)."""
    hits = []
    for line in _git("remote", "-v").splitlines():
        if "@" in line and "://" in line:
            hits.append(("git remote -v", 0, "url_with_credentials", _redact(line)))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--staged", action="store_true", help="scan staged files (pre-commit)")
    g.add_argument("--range", metavar="A..B", help="scan added lines in commit range (pre-push)")
    g.add_argument("--files", nargs="+", metavar="FILE", help="scan explicit files")
    ap.add_argument("--no-remote-check", action="store_true", help="skip `git remote -v` credential check")
    args = ap.parse_args()

    try:
        if args.staged:
            hits = scan_files(files_from_staged())
        elif args.range:
            hits = scan_range(args.range)
        elif args.files:
            hits = scan_files([Path(f) for f in args.files])
        else:
            hits = scan_files(files_from_tree())
        if not args.no_remote_check:
            hits.extend(scan_remote_urls())
    except Exception as exc:  # noqa: BLE001
        print(f"secret_scan: runtime error: {exc}", file=sys.stderr)
        return 2

    if hits:
        print(f"⛔ secret_scan: {len(hits)} hit(s)")
        for where, ln, name, redacted in hits:
            loc = f"{where}:{ln}" if ln else where
            print(f"  [{name}] {loc}: {redacted}")
        print("\nRefusing. Remove the secret, rotate it, then retry.")
        return 1
    print("✅ secret_scan: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
