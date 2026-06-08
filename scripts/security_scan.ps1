# Security Scan Script
# Checks project for accidentally committed secrets

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host "=== Security Scan ==="
Write-Host ""

$ErrorCount = 0
$WarningCount = 0

# 1. Check if .env is in Git
Write-Host "[1/5] Checking .env in Git..."
$EnvInGit = git -C $Root ls-files .env 2>&1
if ($EnvInGit -eq ".env") {
    Write-Host "  ERROR: .env is committed to Git!" -ForegroundColor Red
    $ErrorCount++
} else {
    Write-Host "  OK: .env is not committed" -ForegroundColor Green
}

# 2. Check for API key patterns in tracked files
Write-Host ""
Write-Host "[2/5] Searching for API key patterns..."

$AllFiles = git -C $Root ls-files
$FoundSecrets = 0

# Check for sk- keys (OpenAI, ProxyAPI)
$SkMatches = Select-String -Path $AllFiles -Pattern "sk-[a-zA-Z0-9]{20,}" -ErrorAction SilentlyContinue
foreach ($match in $SkMatches) {
    if ($match.Path -notmatch "example|\.md$") {
        Write-Host "  WARNING: Possible API key in $($match.Path):$($match.LineNumber)" -ForegroundColor Yellow
        $FoundSecrets++
        $WarningCount++
    }
}

# Check for JWT tokens
$JwtMatches = Select-String -Path $AllFiles -Pattern "eyJ[a-zA-Z0-9_-]*\.eyJ" -ErrorAction SilentlyContinue
foreach ($match in $JwtMatches) {
    if ($match.Path -notmatch "example|\.md$") {
        Write-Host "  WARNING: Possible JWT token in $($match.Path):$($match.LineNumber)" -ForegroundColor Yellow
        $FoundSecrets++
        $WarningCount++
    }
}

if ($FoundSecrets -eq 0) {
    Write-Host "  OK: No secret patterns found" -ForegroundColor Green
}

# 3. Check .gitignore
Write-Host ""
Write-Host "[3/5] Checking .gitignore..."

$GitIgnorePath = "$Root/.gitignore"
if (Test-Path $GitIgnorePath) {
    $GitIgnoreContent = Get-Content $GitIgnorePath -Raw
    
    if ($GitIgnoreContent -match '\.env' -and $GitIgnoreContent -match '\*\.pem' -and $GitIgnoreContent -match '\*\.key') {
        Write-Host "  OK: .gitignore has required patterns" -ForegroundColor Green
    } else {
        Write-Host "  WARNING: .gitignore missing some patterns" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host "  ERROR: .gitignore not found!" -ForegroundColor Red
    $ErrorCount++
}

# 4. Check for real keys in .env.example
Write-Host ""
Write-Host "[4/5] Checking .env.example for real keys..."

$ExamplePath = "$Root/.env.example"
if (Test-Path $ExamplePath) {
    $ExampleContent = Get-Content $ExamplePath -Raw
    
    if ($ExampleContent -match "sk-[a-zA-Z0-9]{30,}" -or $ExampleContent -match "ghp_[a-zA-Z0-9]{36}") {
        Write-Host "  ERROR: REAL key found in .env.example!" -ForegroundColor Red
        $ErrorCount++
    } else {
        Write-Host "  OK: .env.example has only placeholders" -ForegroundColor Green
    }
} else {
    Write-Host "  WARNING: .env.example not found" -ForegroundColor Yellow
    $WarningCount++
}

# 5. Check logs for secrets
Write-Host ""
Write-Host "[5/5] Searching logs for secrets..."

$LogFiles = Get-ChildItem -Path $Root -Filter "*.log" -Recurse -ErrorAction SilentlyContinue
$LogsWithSecrets = 0

foreach ($logFile in $LogFiles) {
    try {
        $logContent = Get-Content $logFile -Raw -ErrorAction SilentlyContinue
        if ($logContent -match "api.?key|token|secret|password" -and $logContent -match "[a-zA-Z0-9]{20,}") {
            Write-Host "  WARNING: Log may contain secrets: $($logFile.Name)" -ForegroundColor Yellow
            $LogsWithSecrets++
            $WarningCount++
        }
    } catch {
        # Skip files that cannot be read
    }
}

if ($LogsWithSecrets -eq 0) {
    Write-Host "  OK: Logs do not contain obvious secrets" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "=== Summary ==="

if ($ErrorCount -gt 0) {
    Write-Host "ERROR: CRITICAL ERRORS: $ErrorCount" -ForegroundColor Red
    Write-Host "Project NOT READY for commit/push!" -ForegroundColor Red
    exit 1
} elseif ($WarningCount -gt 0) {
    Write-Host "WARNING: WARNINGS: $WarningCount" -ForegroundColor Yellow
    Write-Host "Recommended to fix before push" -ForegroundColor Yellow
} else {
    Write-Host "OK: ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "Project ready for commit/push" -ForegroundColor Green
}

Write-Host ""
Write-Host "For detailed security info see SECURITY.md"
Write-Host ""
