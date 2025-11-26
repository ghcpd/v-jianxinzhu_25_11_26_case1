Param()
Write-Host "Cleaning virtual environment and caches"
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .venv, .pytest_cache, dist, build, "*.egg-info"
Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Clean complete"
