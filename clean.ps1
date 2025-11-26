# clean.ps1 - Clean up environment on Windows

Write-Host "Cleaning up environment..." -ForegroundColor Green

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Remove virtual environment
if (Test-Path "$ScriptDir\venv") {
    Write-Host "Removing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "$ScriptDir\venv"
    Write-Host "Virtual environment removed" -ForegroundColor Green
} else {
    Write-Host "Virtual environment not found, skipping..." -ForegroundColor Yellow
}

# Remove __pycache__ directories
Write-Host "Removing __pycache__ directories..." -ForegroundColor Yellow
Get-ChildItem -Path $ScriptDir -Recurse -Directory -Name __pycache__ | ForEach-Object {
    Remove-Item -Recurse -Force (Join-Path $ScriptDir $_)
}

# Remove .pytest_cache
if (Test-Path "$ScriptDir\.pytest_cache") {
    Write-Host "Removing .pytest_cache..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "$ScriptDir\.pytest_cache"
}

# Remove htmlcov
if (Test-Path "$ScriptDir\htmlcov") {
    Write-Host "Removing htmlcov directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "$ScriptDir\htmlcov"
}

# Remove .coverage
if (Test-Path "$ScriptDir\.coverage") {
    Write-Host "Removing .coverage file..." -ForegroundColor Yellow
    Remove-Item -Force "$ScriptDir\.coverage"
}

Write-Host "`nCleanup completed successfully!" -ForegroundColor Green
exit 0
