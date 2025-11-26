Param(
    [string]$Venv = ".venv"
)

if (-Not (Test-Path "$Venv\Scripts\python.exe")) {
    Write-Error "Virtual environment not found. Run setup.ps1 first."
    exit 1
}

Write-Host "Running user_display_optimized.py and timing operations..."
& "$Venv\Scripts\python.exe" user_display_optimized.py
