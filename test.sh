#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
pytest --cov=user_display_optimized --cov-report=term-missing
