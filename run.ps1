Param()
if (Test-Path -Path .venv) {
    & .\.venv\Scripts\python.exe -m user_display_optimized
} else {
    python -m user_display_optimized
}
