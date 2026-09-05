#!/usr/bin/env python3
"""
path_scan.py — portable absolute-path scanner (R07 / R18).

Flags anything that ties the repository to one machine:
  * file:///...                       (browser-only links, break on GitHub)
  * C:\\..., d:\\..., D:/...           (Windows drive paths)
  * /Users/<name>/, /home/<name>/     (Unix home paths)
  * \\\\server\\share                 (UNC)

Usage:
  python .governance/path_scan.py                 # tracked files
  python .governance/path_scan.py --staged        # staged files (pre-commit)
  python .governance/path_scan.py --files f1 f2

Exit 0 = clean, 1 = hits, 2 = error.
Exemptions:
  * files listed in EXEMPT_FILES (historical ledger, this scanner, the review that quotes paths)
  * any line containing the marker  path-scan:allow
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PATTERNS = [
    ("file_uri", re.compile(r"file:///")),
    ("windows_drive", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/](?:Users|SMS|Windows|Program Files|[^\s`'\"|)]{2,})")),
    ("unix_home", re.compile(r"(?<![\w/])/(?:Users|home)/[A-Za-z0-9._-]+/")),
    ("unc_path", re.compile(r"\\\\[A-Za-z0-9._-]+\\[A-Za-z0-9._$-]+")),
]

SCAN_SUFFIXES = {".md", ".py", ".ps1", ".sh", ".json", ".yml", ".yaml", ".toml", ".txt", ".cfg", ".ini"}
SKIP_PARTS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
EXEMPT_FILES = {
    # Archival ledger: historical record, allowed to quote old machine paths.
    "proposed_files/GLOBAL_HISTORICAL_LEDGER.md",
    "docs/GLOBAL_HISTORICAL_LEDGER.md",
    # This scanner documents what it rejects.
    ".governance/path_scan.py",
    # Audit reports quote offending paths as evidence.
    "docs/audit_reports/context-connect/context-connect.MD",
    "docs/audit_reports/context-connect/context_connect_2026-09-05.patch",
}
EXEMPT_DIRS = ("docs/audit_reports/", "context-connect/")
ALLOW_MARKER = "path-scan:allow"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def _is_exempt(p: Path) -> bool:
    s = p.as_posix()
    return s in EXEMPT_FILES or any(s.startswith(d) for d in EXEMPT_DIRS)


def scan_files(paths: list[Path]) -> list[tuple[str, int, str, str]]:
    hits = []
    for p in paths:
        if p.suffix.lower() not in SCAN_SUFFIXES or any(part in SKIP_PARTS for part in p.parts):
            continue
        if _is_exempt(p) or not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if ALLOW_MARKER in line:
                continue
            for name, rx in PATTERNS:
                if rx.search(line):
                    hits.append((p.as_posix(), i, name, line.strip()[:160]))
                    break
    return hits


def files_from_tree() -> list[Path]:
    return [Path(p) for p in _git("ls-files", "-z").split("\0") if p]


def files_from_staged() -> list[Path]:
    return [Path(p) for p in _git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split("\0") if p]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--staged", action="store_true")
    g.add_argument("--files", nargs="+", metavar="FILE")
    args = ap.parse_args()
    try:
        if args.staged:
            hits = scan_files(files_from_staged())
        elif args.files:
            hits = scan_files([Path(f) for f in args.files])
        else:
            hits = scan_files(files_from_tree())
    except Exception as exc:  # noqa: BLE001
        print(f"path_scan: runtime error: {exc}", file=sys.stderr)
        return 2

    if hits:
        print(f"⛔ path_scan: {len(hits)} machine-specific path(s)")
        for f, ln, name, line in hits:
            print(f"  [{name}] {f}:{ln}: {line}")
        print("\nUse repo-relative paths, CLI args, or environment variables instead.")
        return 1
    print("✅ path_scan: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
