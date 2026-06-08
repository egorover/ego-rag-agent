# Pre-push checks: merge conflicts, secrets, syntax, tests
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔒 ego-rag-agent: pre-push security & quality checks" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# 1. Security Scan
# ═══════════════════════════════════════════════════════════════
Write-Host "[1/5] Запуск сканирования безопасности..." -ForegroundColor Yellow
& "$Root/security_scan.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Security scan FAILED - fix issues before push!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# 2. Merge Conflict Markers
# ═══════════════════════════════════════════════════════════════
Write-Host "[2/5] Проверка на конфликты слияния..." -ForegroundColor Yellow
$pyFiles = Get-ChildItem -Recurse -Include *.py -File |
    Where-Object { $_.FullName -notmatch '\\\.venv\\|\\chroma_db\\|__pycache__' }
$conflictMarkers = $pyFiles | Select-String -Pattern '<<<<<<<|=======|>>>>>>>' -ErrorAction SilentlyContinue
if ($conflictMarkers) {
    Write-Host "[FAIL] Merge conflict markers found" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] No merge conflict markers" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════════
# 3. .env Git Tracking
# ═══════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[3/5] Проверка .env в Git..." -ForegroundColor Yellow
$envTracked = git ls-files .env 2>$null
if ($envTracked) {
    Write-Host "[FAIL] .env is tracked by git - REMOVE IT!" -ForegroundColor Red
    exit 1
}
git check-ignore -q .env 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] .env is properly gitignored" -ForegroundColor Green
} else {
    Write-Host "[WARN] .env exists but is not in .gitignore" -ForegroundColor Yellow
}

# ═══════════════════════════════════════════════════════════════
# 4. Python Syntax Check
# ═══════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[4/5] Проверка синтаксиса Python..." -ForegroundColor Yellow
python -m compileall -q .
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Python syntax errors found" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python syntax valid" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════════
# 5. Tests
# ═══════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "[5/5] Запуск тестов..." -ForegroundColor Yellow
python -m pytest tests/ -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Tests failed" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] All tests passed" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ ALL CHECKS PASSED - Ready for push!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "Помните о безопасности:"
Write-Host "  • Никогда не коммитьте .env"
Write-Host "  • Ротируйте ключи каждые 90 дней"
Write-Host "  • Используйте секрет-менеджер для production"
Write-Host ""
