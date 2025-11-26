#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
source .venv/bin/activate

pytest --cov=user_display_optimized --cov-report=term-missing
