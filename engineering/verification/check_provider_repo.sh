#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/../.." || exit 2
FAIL=0
# Remove transient local tool caches before verification; they must not be tracked.
find . -path ./.git -prune -o -type d \( -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache -o -name .ruff_cache \) -prune -exec rm -rf {} + 2>/dev/null || true
pass() { printf 'PASS: %s\n' "$*"; }
fail() { FAIL=1; printf 'FAIL: %s\n' "$*"; }

for f in \
  README.md \
  pyproject.toml \
  docs/provider_references/final_docs_v3/30_PROVIDER_ARCHITECTURE_AND_PLUGIN_SPEC.md \
  docs/provider_references/final_docs_v3/31_PROVIDER_SCAFFOLDING_AND_ONBOARDING.md \
  core/contracts/providers.py \
  tests/contract/test_provider_contracts.py; do
  [ -f "$f" ] && pass "exists: $f" || fail "missing: $f"
done

if find . -path ./.git -prune -o \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.mypy_cache' -o -name '.ruff_cache' \) -print | grep -q .; then
  fail "cache directory present after cleanup"
else
  pass "no cache directories present"
fi

if grep -rEn 'AKIA[0-9A-Z]{16}|-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----|xox[bap]-[0-9A-Za-z-]{10,}|ghp_[0-9A-Za-z]{36}|sk-[A-Za-z0-9]{40,}' \
   --include='*.md' --include='*.py' --include='*.sh' --include='*.yml' --include='*.yaml' --include='*.json' --include='*.txt' . --exclude-dir=.git >/dev/null 2>&1; then
  fail "possible secret detected"
else
  pass "secret scan clean"
fi

if [ "$FAIL" -eq 0 ]; then
  printf 'RESULT: PASS\n'
  exit 0
fi
printf 'RESULT: FAIL\n'
exit 1
