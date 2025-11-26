param()
Write-Host "Cleaning environment..."
if (Test-Path ".venv") { Remove-Item -Recurse -Force .venv }
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force __pycache__ }
if (Test-Path "tests\__pycache__") { Remove-Item -Recurse -Force tests\__pycache__ }
if (Test-Path ".coverage") { Remove-Item -Force .coverage }
Write-Host "[INFO] Cleaned environment"