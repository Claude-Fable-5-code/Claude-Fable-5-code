#!/usr/bin/env bash
# One-shot installer: points git at the versioned hooks directory. Idempotent.
set -eu
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
git config core.hooksPath .governance/hooks
chmod +x .governance/hooks/* .governance/*.py 2>/dev/null || true
echo "core.hooksPath = $(git config core.hooksPath)"
echo "Hooks installed. Proof: git config core.hooksPath  ->  .governance/hooks"
