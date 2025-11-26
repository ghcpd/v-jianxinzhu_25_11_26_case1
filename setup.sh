#!/usr/bin/env bash
set -euo pipefail

# Determine python interpreter
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  PYTHON=python
fi

# Create venv if missing
if [ ! -d .venv ]; then
  echo "[setup] Creating virtual environment (.venv) with $PYTHON"
  "$PYTHON" -m venv .venv
fi

# Activate
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

echo "[setup] Done. Activate with: source .venv/bin/activate"
