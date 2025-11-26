$ErrorActionPreference = "Stop"

function Get-Python {
    $candidates = @('py -3', 'python3', 'python')
    foreach ($cmd in $candidates) {
        try {
            $version = & $cmd --version 2>$null
            if ($LASTEXITCODE -eq 0) { return $cmd }
        } catch {}
    }
    throw "No suitable Python interpreter found. Install Python 3.10+ and retry."
}

$python = Get-Python

if (-not (Test-Path .venv)) {
    Write-Host "[setup] Creating virtual environment (.venv) with $python"
    & $python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "[setup] Done. Activate with: .\\.venv\\Scripts\\Activate.ps1"
