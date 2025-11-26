# run.ps1 - Run optimized user display module with timing on Windows

param(
    [string]$Module = "user_display_optimized"
)

Write-Host "Running optimized user display module..." -ForegroundColor Green

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

# Run with timing
Write-Host "Execution started at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')" -ForegroundColor Yellow

$StopWatch = [System.Diagnostics.Stopwatch]::StartNew()

& python "$ScriptDir\$Module.py"

$StopWatch.Stop()
$ElapsedMs = $StopWatch.Elapsed.TotalMilliseconds

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Execution completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')" -ForegroundColor Yellow
Write-Host "Total execution time: $([Math]::Round($ElapsedMs, 2))ms" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

exit 0
