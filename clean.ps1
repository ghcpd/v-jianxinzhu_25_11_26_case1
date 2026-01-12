# Clean script - Remove virtual environment and generated files
# Works on Windows PowerShell

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Cleaning Environment" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Remove virtual environment
if (Test-Path "venv") {
    Write-Host "Removing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}

# Remove pytest cache
if (Test-Path ".pytest_cache") {
    Write-Host "Removing pytest cache..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .pytest_cache
}

# Remove coverage files
if (Test-Path "htmlcov") {
    Write-Host "Removing coverage reports..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force htmlcov
}

if (Test-Path ".coverage") {
    Remove-Item -Force .coverage
}

# Remove Python cache
if (Test-Path "__pycache__") {
    Write-Host "Removing Python cache..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force __pycache__
}

if (Test-Path "tests\__pycache__") {
    Remove-Item -Recurse -Force tests\__pycache__
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "To set up again, run:" -ForegroundColor Cyan
Write-Host "  powershell -File setup.ps1" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Green

exit 0
