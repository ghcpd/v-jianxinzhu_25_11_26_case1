#!/usr/bin/env bash
set -euo pipefail

rm -rf .venv .pytest_cache .coverage
find . -name "__pycache__" -type d -prune -exec rm -rf {} +

echo "[clean] Environment cleaned."
