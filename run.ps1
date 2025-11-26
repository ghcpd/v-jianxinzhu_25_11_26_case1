param()
if (Test-Path ".venv") {
    . ".\.venv\Scripts\Activate.ps1"
}
python user_display_optimized.py
