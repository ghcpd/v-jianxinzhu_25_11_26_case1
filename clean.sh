#!/usr/bin/env bash
set -euo pipefail

echo "Cleaning project artifacts..."
rm -rf .venv
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
rm -rf .pytest_cache
echo "Clean complete."
