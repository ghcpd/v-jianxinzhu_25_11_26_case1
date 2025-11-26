#!/usr/bin/env bash
set -euo pipefail

VENV=${VENV:-.venv}
PY="${VENV}/bin/python"

if [ ! -x "${PY}" ]; then
  echo "Virtual environment not found. Run setup.sh first." >&2
  exit 1
fi

echo "Running user_display_optimized.py and timing operations..."
"${PY}" user_display_optimized.py
