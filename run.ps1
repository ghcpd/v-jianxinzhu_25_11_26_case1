# Run script - Execute the optimized module
# Works on Windows PowerShell

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Running User Display Optimizer" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "Error: Virtual environment not found" -ForegroundColor Red
    Write-Host "Please run: powershell -File setup.ps1" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run the optimized module
Write-Host "Executing user_display_optimized.py..." -ForegroundColor Yellow
Write-Host ""
python user_display_optimized.py

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Execution complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

exit 0
