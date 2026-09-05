# One-shot installer for Windows (PowerShell). Idempotent.
$root = git rev-parse --show-toplevel
Set-Location $root
git config core.hooksPath .governance/hooks
Write-Host "core.hooksPath = $(git config core.hooksPath)"
Write-Host "Hooks installed. Note: Git for Windows runs bash hooks via its bundled sh.exe; python3 or python must be on PATH."
