#!/usr/bin/env python3
"""
verify_sync.py — compatibility shim (R17/R18).

The parity engine moved to .governance/verify_sync.py and is fully portable:
  python .governance/verify_sync.py --master <workspace>      # or FABLE_MASTER env
This shim forwards all arguments so existing docs/commands keep working.
"""
import runpy
import sys
from pathlib import Path

sys.argv[0] = str(Path(__file__).resolve().parent / ".governance" / "verify_sync.py")
runpy.run_path(sys.argv[0], run_name="__main__")
