# Test script - Run tests with coverage
# Works on Windows PowerShell

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Running Tests with Coverage" -ForegroundColor Cyan
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

# Run tests with coverage
Write-Host "Running pytest with coverage..." -ForegroundColor Yellow
Write-Host ""
pytest tests/ -v --cov=user_display_optimized --cov-report=term-missing --cov-report=html

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Tests complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "Coverage report saved to htmlcov\index.html" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Green

exit 0
