Param(
    [string]$Venv = ".venv"
)

if (-Not (Test-Path "$Venv\Scripts\python.exe")) {
    Write-Error "Virtual environment not found. Run setup.ps1 first."
    exit 1
}

Write-Host "Running tests with coverage..."
& "$Venv\Scripts\python.exe" -m pytest --maxfail=1 --disable-warnings -q --cov=user_display_optimized --cov-report=term --cov-fail-under=85
