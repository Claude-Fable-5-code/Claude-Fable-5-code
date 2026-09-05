#!/usr/bin/env sh
# Reset-resistant fallback when the sandbox has no push permission (Rule 4: never claim "pushed").
# Produces ONE archive (bundle + patches) in /tmp; the agent then uploads it to blob storage and
# pastes the URL in the handoff. Owner applies: tar xzf …; git am 0*.patch; git push origin <branch>
# Usage: sh .governance/export_bundle.sh
set -e
BR="$(git rev-parse --abbrev-ref HEAD)"; OUT="/tmp/export_${BR}"; rm -rf "$OUT"; mkdir -p "$OUT"
git bundle create "$OUT/${BR}.bundle" "origin/main..${BR}" 2>/dev/null
git format-patch -q origin/main -o "$OUT" >/dev/null
tar -czf "/tmp/${BR}_$(date +%Y-%m-%d).tar.gz" -C "$OUT" .
echo "exported $(git rev-list --count origin/main..HEAD) commit(s) → /tmp/${BR}_$(date +%Y-%m-%d).tar.gz (HEAD=$(git rev-parse --short HEAD))"
