#!/usr/bin/env bash
set -euo pipefail

echo "Removing virtual environment (.venv) and caches"
rm -rf .venv .pytest_cache dist build *.egg-info __pycache__
find . -name '__pycache__' -type d -prune -exec rm -rf {} + || true
echo "Clean complete"
