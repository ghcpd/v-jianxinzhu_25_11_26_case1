$ErrorActionPreference = "Stop"
& .\.venv\Scripts\Activate.ps1

pytest --cov=user_display_optimized --cov-report=term-missing
