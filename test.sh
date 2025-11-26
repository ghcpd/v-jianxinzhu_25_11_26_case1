#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

# Run tests with coverage and require a minimum coverage of 85%
pytest --maxfail=1 -q --cov=user_display_optimized --cov-report=term-missing --cov-fail-under=85
