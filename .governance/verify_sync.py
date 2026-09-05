#!/usr/bin/env python3
"""
verify_sync.py — portable parity gate (R17 / R18).

Verifies SHA-256 parity (CRLF-normalised) between three layers:

  A. proposed_files/<name>           (the package pushed to GitHub)
  B. <published repo root>/<path>    (README.md, AGENTS.md, ... at repo root)   [always]
  C. <master workspace>/<path>       (the agent's private working tree)          [optional]

Layer C is only checked when a master path is supplied — via --master or the
environment variable FABLE_MASTER — so the script is runnable on any machine
(CI, consultant, sandbox) without editing it. NOTHING is hard-coded.

Usage:
  python .governance/verify_sync.py                          # A vs B only
  python .governance/verify_sync.py --master /path/to/master # A vs B vs C
  FABLE_MASTER=/path/to/master python .governance/verify_sync.py
  python .governance/verify_sync.py --list                   # print mapping

Exit 0 = full parity, 1 = drift or missing file, 2 = usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# proposed_files name  ->  canonical path inside master workspace / published repo
MAPPING: dict[str, str] = {
    "00-bolla-constitution.md": ".agents/rules/00-bolla-constitution.md",
    "00-RULES.md": ".agents/rules/00-RULES.md",
    "AGENT.md": ".agents/AGENT.md",
    "AGENTS.md": ".agents/AGENTS.md",
    "planning_skill.md": ".agents/skills/02-planning-system/SKILL.md",
    "init_root.py": ".agents/tools/init_root.py",
    "00-planning.md": ".agents/workflows/00-planning.md",
    "00-sequential-requests.md": ".agents/workflows/00-sequential-requests.md",
    "00-speckit.md": ".agents/workflows/00-speckit.md",
    "GEMINI.md": "GEMINI.md",
    "README.md": "README.md",
    "ROOT_AGENTS_POINTER.md": "AGENTS.md",
    "ROOT_PROGRESS_POINTER.md": "PROGRESS.md",
    "Root_ANCHORS.md": "Root/ANCHORS.md",
    "PROGRESS.md": "Root/PROGRESS.md",
}

# Files that must ALSO be identical between proposed_files/ and the published repo root.
# This is the drift the original R17 request was about and the first engine skipped.
# NOTE: the repo-root README.md is the *review-repo landing page*, intentionally different
# from proposed_files/README.md (the project README). It is therefore NOT paired here.
PUBLISHED_PAIRS: dict[str, str] = {
    ".gitignore": ".gitignore",
}


def sha256_norm(p: Path) -> tuple[str, int]:
    raw = p.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest(), len(raw.splitlines())


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for cand in (here.parent.parent, Path.cwd()):
        if (cand / "proposed_files").is_dir():
            return cand
    return here.parent.parent


def compare(label: str, a: Path, b: Path) -> bool:
    if not a.is_file():
        print(f"❌ MISSING  {label}: {a}")
        return False
    if not b.is_file():
        print(f"❌ MISSING  {label}: {b}")
        return False
    ha, la = sha256_norm(a)
    hb, lb = sha256_norm(b)
    if ha == hb:
        print(f"✅ MATCH    [{la:3d} lines] {label}")
        return True
    print(f"❌ DRIFT    {label}: {la} vs {lb} lines | {ha[:12]}… vs {hb[:12]}…")
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=None, help="published repo root (default: auto-detect)")
    ap.add_argument("--proposed", default=None, help="proposed_files dir (default: <repo>/proposed_files)")
    ap.add_argument("--master", default=os.environ.get("FABLE_MASTER"),
                    help="master workspace root (default: $FABLE_MASTER; omitted → layer C skipped)")
    ap.add_argument("--list", action="store_true", help="print mapping and exit")
    args = ap.parse_args()

    if args.list:
        for k, v in MAPPING.items():
            print(f"proposed_files/{k:32s} -> {v}")
        return 0

    repo = Path(args.repo).resolve() if args.repo else repo_root()
    proposed = Path(args.proposed).resolve() if args.proposed else repo / "proposed_files"
    master = Path(args.master).resolve() if args.master else None

    if not proposed.is_dir():
        print(f"verify_sync: proposed_files not found at {proposed}", file=sys.stderr)
        return 2

    print("=== verify_sync (portable) ===")
    print(f"repo     : {repo}")
    print(f"proposed : {proposed}")
    print(f"master   : {master if master else '(not supplied — layer C skipped)'}")
    print()

    ok = total = 0

    print("--- Layer A↔B: proposed_files vs published repo root ---")
    for name, pub in PUBLISHED_PAIRS.items():
        total += 1
        ok += compare(f"proposed_files/{name} == {pub}", proposed / name, repo / pub)

    if master:
        if not master.is_dir():
            print(f"verify_sync: master path does not exist: {master}", file=sys.stderr)
            return 2
        print("\n--- Layer A↔C: proposed_files vs master workspace ---")
        for name, rel in MAPPING.items():
            total += 1
            ok += compare(f"proposed_files/{name} == master/{rel}", proposed / name, master / rel)

    print(f"\nRESULT: {ok}/{total} in parity")
    if ok != total:
        print("⛔ PARITY FAILED — do not push.")
        return 1
    print("🎉 PARITY PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
