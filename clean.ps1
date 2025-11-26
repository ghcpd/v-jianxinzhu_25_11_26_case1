$ErrorActionPreference = "Stop"

if (Test-Path .venv) { Remove-Item .venv -Recurse -Force }
if (Test-Path .pytest_cache) { Remove-Item .pytest_cache -Recurse -Force }
if (Test-Path .coverage) { Remove-Item .coverage -Force }

Get-ChildItem -Recurse -Directory -Filter "__pycache__" | ForEach-Object { Remove-Item $_.FullName -Recurse -Force }

Write-Host "[clean] Environment cleaned."
