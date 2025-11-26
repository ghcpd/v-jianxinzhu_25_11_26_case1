param()
Write-Host "Setting up virtualenv and installing dependencies..."
python -m venv .venv
$activate = Join-Path -Path .venv -ChildPath "Scripts\Activate.ps1"
. $activate
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "[INFO] Virtualenv set up. Activate with: .\.venv\Scripts\Activate.ps1"