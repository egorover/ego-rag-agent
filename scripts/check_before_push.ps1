# Pre-push checks: merge conflicts, secrets, syntax, tests
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "=== ego-rag-agent: pre-push check ===" -ForegroundColor Cyan

$pyFiles = Get-ChildItem -Recurse -Include *.py -File |
    Where-Object { $_.FullName -notmatch '\\\.venv\\|\\chroma_db\\|__pycache__' }
$conflictMarkers = $pyFiles | Select-String -Pattern '<<<<<<<|=======|>>>>>>>' -ErrorAction SilentlyContinue
if ($conflictMarkers) {
    Write-Host "[FAIL] Merge conflict markers found" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] No merge conflict markers"

$envTracked = git ls-files .env 2>$null
if ($envTracked) {
    Write-Host "[FAIL] .env is tracked by git" -ForegroundColor Red
    exit 1
}
git check-ignore -q .env 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] .env is gitignored"
} else {
    Write-Host "[WARN] .env is not in .gitignore" -ForegroundColor Yellow
}

$suspicious = @()
foreach ($f in (git ls-files)) {
    if ($f -match '\.env') { continue }
    $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
    if ($content -match 'sk-[a-zA-Z0-9]{20,}') { $suspicious += $f }
}
if ($suspicious.Count -gt 0) {
    Write-Host "[FAIL] Possible API keys in tracked files" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] No suspicious API key patterns in git"

python -m compileall -q .
if ($LASTEXITCODE -ne 0) { exit 1 }
Write-Host "[OK] Python syntax"

python -m pytest tests/ -q
if ($LASTEXITCODE -ne 0) { exit 1 }
Write-Host "[OK] Tests passed"

Write-Host ""
Write-Host "=== Ready for push ===" -ForegroundColor Green
