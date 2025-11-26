Param()
Write-Host "Idempotent setup for Windows (PowerShell)"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python isn't on PATH. Install Python 3.10+ first."
    exit 2
}

if (-not (Test-Path -Path .venv)) {
    python -m venv .venv
}

Write-Host "Activating virtual environment and installing requirements"
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Setup complete. Activate environment with: .\.venv\Scripts\Activate.ps1"
