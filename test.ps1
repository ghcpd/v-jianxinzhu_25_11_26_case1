Param()
if (Test-Path -Path .venv) {
    & .\.venv\Scripts\python.exe -m pytest --maxfail=1 -q --cov=user_display_optimized --cov-report=term-missing --cov-fail-under=85
} else {
    python -m pytest --maxfail=1 -q --cov=user_display_optimized --cov-report=term-missing --cov-fail-under=85
}
