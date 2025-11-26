# test.ps1 - Run tests with coverage on Windows

param(
    [switch]$Coverage = $false,
    [int]$MinCoverage = 85
)

Write-Host "Running test suite..." -ForegroundColor Green

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if venv exists
$VenvScript = "$ScriptDir\venv\Scripts\Activate.ps1"
if (Test-Path $VenvScript) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & $VenvScript
} else {
    Write-Host "WARNING: Virtual environment not found. Using system Python..." -ForegroundColor Yellow
}

# Build pytest arguments
$PytestArgs = @(
    "$ScriptDir\tests",
    "-v",
    "--tb=short"
)

# Add coverage if requested
if ($Coverage) {
    $PytestArgs += @(
        "--cov=user_display_optimized",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=$MinCoverage"
    )
    Write-Host "Running with coverage (minimum $MinCoverage%)..." -ForegroundColor Yellow
} else {
    Write-Host "Running without coverage..." -ForegroundColor Yellow
}

# Run tests
Write-Host "Execution started at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')" -ForegroundColor Yellow

$StopWatch = [System.Diagnostics.Stopwatch]::StartNew()

& pytest @PytestArgs
$TestExitCode = $LASTEXITCODE

$StopWatch.Stop()
$ElapsedMs = $StopWatch.Elapsed.TotalMilliseconds

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Test execution completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')" -ForegroundColor Yellow
Write-Host "Total execution time: $([Math]::Round($ElapsedMs, 2))ms" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

if ($Coverage) {
    Write-Host "`nHTML coverage report generated at: $ScriptDir\htmlcov\index.html" -ForegroundColor Yellow
}

exit $TestExitCode
