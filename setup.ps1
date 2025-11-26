Param(
    [string]$Python = "python"
)

Write-Host "Setting up Python virtual environment and installing dependencies..."
$Venv = ".venv"

if (-Not (Get-Command $Python -ErrorAction SilentlyContinue)) {
    Write-Error "Python executable not found: $Python"
    exit 2
}

if (-Not (Test-Path $Venv)) {
    & $Python -m venv $Venv
    Write-Host "Created venv: $Venv"
} else {
    Write-Host "Using existing venv: $Venv"
}

& "$Venv\Scripts\python.exe" -m pip install --upgrade pip
& "$Venv\Scripts\python.exe" -m pip install -r requirements.txt
Write-Host "Setup complete. Activate with: . $Venv/Scripts/Activate.ps1"
