#!/usr/bin/env bash
set -euo pipefail

VENV=${VENV:-.venv}
PY="${VENV}/bin/python"

if [ ! -x "${PY}" ]; then
  echo "Virtual environment not found. Run setup.sh first." >&2
  exit 1
fi

echo "Running tests with coverage..."
"${PY}" -m pytest --maxfail=1 --disable-warnings -q --cov=user_display_optimized --cov-report=term --cov-fail-under=85
