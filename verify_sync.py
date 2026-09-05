#!/usr/bin/env python3
"""
verify_sync.py — Parity Verification Engine (R17)
Ensures 100% SHA-256 byte-exact parity between master repository files and proposed_files/.
Fails with exit code 1 if any discrepancy or missing file is found.
"""

import sys
import hashlib
from pathlib import Path

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Mapping: (Master Source Path relative to repo root) -> (proposed_files/ path)
MAPPING = {
    '.agents/rules/00-bolla-constitution.md': '00-bolla-constitution.md',
    'GEMINI.md': 'GEMINI.md',
    '.agents/workflows/00-sequential-requests.md': '00-sequential-requests.md',
    '.agents/AGENTS.md': 'AGENTS.md',
    '.agents/workflows/00-planning.md': '00-planning.md',
    '.agents/skills/02-planning-system/SKILL.md': 'planning_skill.md',
    '.agents/workflows/00-speckit.md': '00-speckit.md',
    '.agents/AGENT.md': 'AGENT.md',
    'README.md': 'README.md',
    '.agents/rules/00-RULES.md': '00-RULES.md',
    'Root/ANCHORS.md': 'Root_ANCHORS.md',
    'Root/PROGRESS.md': 'PROGRESS.md',
    'AGENTS.md': 'ROOT_AGENTS_POINTER.md',
    'PROGRESS.md': 'ROOT_PROGRESS_POINTER.md',
    '.agents/tools/init_root.py': 'init_root.py',
}

def compute_hash(p: Path) -> tuple[str, int]:
    raw = p.read_bytes().replace(b'\r\n', b'\n')
    return hashlib.sha256(raw).hexdigest(), len(raw.splitlines())

def main():
    # Resolve directories
    # If run inside fable_repo:
    # cwd or script directory
    script_dir = Path(__file__).resolve().parent
    if (script_dir / 'proposed_files').exists():
        proposed_base = script_dir / 'proposed_files'
    else:
        proposed_base = Path(r'C:\Users\pc\.gemini\antigravity-ide\brain\e3e815cc-3e42-489d-ba39-82ef7d1a7dd7\scratch\fable_repo\proposed_files')

    master_base = Path(r'd:\SMS\.hRhRhRhRhRhR')

    print(f"=== Running verify_sync.py (Parity Gate R17) ===")
    print(f"Master source : {master_base}")
    print(f"Proposed files: {proposed_base}\n")

    mismatches = 0
    total = len(MAPPING)

    for src_rel, prop_rel in sorted(MAPPING.items()):
        src_path = master_base / src_rel
        prop_path = proposed_base / prop_rel

        if not src_path.exists():
            print(f"❌ MISSING SOURCE: {src_rel} does not exist at {src_path}")
            mismatches += 1
            continue

        if not prop_path.exists():
            print(f"❌ MISSING TARGET: {prop_rel} does not exist at {prop_path}")
            mismatches += 1
            continue

        src_hash, src_lines = compute_hash(src_path)
        prop_hash, prop_lines = compute_hash(prop_path)

        if src_hash == prop_hash:
            print(f" ✅ MATCH   [{prop_lines:3d} lines] {prop_rel:28s} == {src_rel}")
        else:
            print(f" ❌ MISMATCH [{prop_lines:3d} vs {src_lines:3d}] {prop_rel:28s} != {src_rel}")
            print(f"    src : {src_hash}")
            print(f"    prop: {prop_hash}")
            mismatches += 1

    print(f"\nRESULT: {total - mismatches}/{total} verified in 100% parity.")
    if mismatches > 0:
        print(f"⛔ PARITY CHECK FAILED: {mismatches} discrepancy detected!")
        sys.exit(1)
    else:
        print("🎉 PARITY CHECK PASSED: Master workspace and proposed_files are 100% identical!")
        sys.exit(0)

if __name__ == '__main__':
    main()
