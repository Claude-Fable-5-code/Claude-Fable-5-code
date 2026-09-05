#!/usr/bin/env python3
"""
probe_init_root.py — behavioural probe for proposed_files/init_root.py (R02–R05).

This is the consultant's probe, promoted to CI so the agent never has to
self-report "7/7 True" again — the pipeline reports it.

Cases:
  P1  fresh init creates Root/ with the 6 core files + HANDOFF.md
  P2  ai_state.json keys == exact 8-key contract on fresh init
  P3  rerun (answer 'y') preserves user keys and turn_count
  P4  rerun preserves PROGRESS/tasks/memory/HANDOFF contents
  P5  '../x' traversal rejected (rc != 0, nothing created outside WORKSPACE)
  P6  absolute path rejected
  P7  symlink escaping WORKSPACE rejected
  P8  --validate on Root with a missing file -> rc != 0
  P9  --validate on intact Root -> rc == 0

Exit 0 = all pass, 1 = any fail.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CONTRACT = {"mode", "current_tag", "turn_count", "git_commit",
            "last_action", "next_action", "last_message_summary", "last_updated"}
CORE = ["ai_state.json", "PROGRESS.md", "tasks.md", "memory.md", "keys.txt", "ANCHORS.md", "HANDOFF.md"]


def find_script() -> Path:
    here = Path(__file__).resolve().parent.parent
    for cand in (here / "proposed_files" / "init_root.py", Path.cwd() / "proposed_files" / "init_root.py"):
        if cand.is_file():
            return cand
    sys.exit("probe: proposed_files/init_root.py not found")


def main() -> int:
    src = find_script().read_text(encoding="utf-8")
    lab = Path(tempfile.mkdtemp(prefix="probe_init_root_"))
    results: list[tuple[str, bool, str]] = []

    def rec(name: str, ok: bool, note: str = "") -> None:
        results.append((name, ok, note))

    try:
        ws = lab / "WORKSPACE"
        (ws / ".agents" / "skills").mkdir(parents=True)
        script = ws / ".agents" / "skills" / "init_root.py"
        script.write_text(src, encoding="utf-8")

        def run(args: list[str], stdin: str = "") -> subprocess.CompletedProcess:
            return subprocess.run([sys.executable, str(script), *args], input=stdin, capture_output=True,
                                  text=True, encoding="utf-8", errors="replace", cwd=ws, timeout=60)

        # P1 / P2
        (ws / "proj").mkdir()
        r = run(["--project", "proj"])
        root = ws / "proj" / "Root"
        missing = [f for f in CORE if not (root / f).is_file()]
        rec("P1 fresh init creates core files + HANDOFF", r.returncode == 0 and not missing, f"rc={r.returncode} missing={missing}")
        st = root / "ai_state.json"
        keys = set(json.loads(st.read_text(encoding="utf-8"))) if st.is_file() else set()
        rec("P2 ai_state keys == 8-key contract", keys == CONTRACT, f"extra={sorted(keys - CONTRACT)} missing={sorted(CONTRACT - keys)}")

        # P3 / P4
        st.write_text(json.dumps({"mode": "[CODING]", "marker": "KEEP", "turn_count": 42}), encoding="utf-8")
        for f in ("PROGRESS.md", "tasks.md", "memory.md", "HANDOFF.md"):
            (root / f).write_text(f"USER_EDITED_{f}", encoding="utf-8")
        r = run(["--project", "proj"], "y\n")
        d = json.loads(st.read_text(encoding="utf-8"))
        rec("P3 rerun preserves user key + turn_count", d.get("marker") == "KEEP" and d.get("turn_count") == 42 and d.get("mode") == "[CODING]",
            f"rc={r.returncode} marker={d.get('marker')} turn={d.get('turn_count')}")
        kept = [f for f in ("PROGRESS.md", "tasks.md", "memory.md", "HANDOFF.md") if "USER_EDITED" in (root / f).read_text(encoding="utf-8")]
        rec("P4 rerun preserves ledgers", len(kept) == 4, f"kept={kept}")

        # P5 traversal
        r = run(["--project", "../escaped"])
        rec("P5 traversal '../' rejected", r.returncode != 0 and not (lab / "escaped").exists(), f"rc={r.returncode}")

        # P6 absolute
        abs_target = lab / "abs_target"
        r = run(["--project", str(abs_target)])
        rec("P6 absolute path rejected", r.returncode != 0 and not (abs_target / "Root").exists(), f"rc={r.returncode}")

        # P7 symlink escape
        outside = lab / "outside"; outside.mkdir()
        link = ws / "linkproj"
        try:
            os.symlink(outside, link, target_is_directory=True)
            r = run(["--project", "linkproj"])
            rec("P7 symlink escape rejected", r.returncode != 0 and not (outside / "Root").exists(), f"rc={r.returncode}")
        except (OSError, NotImplementedError) as exc:
            rec("P7 symlink escape rejected", True, f"skipped (symlink unsupported: {exc})")

        # P8 / P9 verify
        (ws / "vproj").mkdir(); run(["--project", "vproj"])
        r_ok = run(["--project", "vproj", "--validate"])
        (ws / "vproj" / "Root" / "tasks.md").unlink()
        r_bad = run(["--project", "vproj", "--validate"])
        rec("P8 --validate missing file -> rc!=0", r_bad.returncode != 0, f"rc={r_bad.returncode}")
        rec("P9 --validate intact -> rc==0", r_ok.returncode == 0, f"rc={r_ok.returncode}")
    finally:
        shutil.rmtree(lab, ignore_errors=True)

    passed = sum(ok for _, ok, _ in results)
    for name, ok, note in results:
        print(f"{'✅' if ok else '❌'} {name}  ({note})")
    print(f"\nRESULT: {passed}/{len(results)}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
