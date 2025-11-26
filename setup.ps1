# setup.ps1 - Setup virtual environment and install dependencies on Windows

param(
    [string]$PythonVersion = "python"
)

Write-Host "Setting up Python environment..." -ForegroundColor Green

# Check if Python is available
try {
    $PythonExe = & where.exe python 2>$null
    if (-not $?) {
        Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Python executable: $PythonExe" -ForegroundColor Yellow

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if venv already exists
if (Test-Path "$ScriptDir\venv") {
    Write-Host "Virtual environment already exists. Skipping venv creation..." -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & python -m venv "$ScriptDir\venv"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$VenvScript = "$ScriptDir\venv\Scripts\Activate.ps1"

if (-not (Test-Path $VenvScript)) {
    Write-Host "ERROR: Virtual environment activation script not found" -ForegroundColor Red
    exit 1
}

& $VenvScript

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& python -m pip install --upgrade pip

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: pip upgrade encountered issues but continuing..." -ForegroundColor Yellow
}

# Install requirements
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
if (Test-Path "$ScriptDir\requirements.txt") {
    & pip install -r "$ScriptDir\requirements.txt"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install requirements" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ERROR: requirements.txt not found" -ForegroundColor Red
    exit 1
}

Write-Host "`nSetup completed successfully!" -ForegroundColor Green
Write-Host "Virtual environment is at: $ScriptDir\venv" -ForegroundColor Yellow
Write-Host "To activate manually, run: $VenvScript" -ForegroundColor Yellow
exit 0
