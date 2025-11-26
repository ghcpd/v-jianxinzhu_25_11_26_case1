#!/usr/bin/env bash
set -euo pipefail

# Idempotent environment setup for Unix-like systems (macOS / Linux)
PY=python3
if ! command -v "$PY" >/dev/null 2>&1; then
  PY=python
fi

if ! command -v "$PY" >/dev/null 2>&1; then
  echo "Python not found. Please install Python 3.10+ and re-run."
  exit 2
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment in .venv"
  $PY -m venv .venv
fi

echo "Activating virtual environment and installing requirements"
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Setup complete. Activate with: source .venv/bin/activate"
