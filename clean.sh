#!/usr/bin/env bash
set -euo pipefail

rm -rf .venv
rm -rf __pycache__
rm -rf tests/__pycache__
rm -f .coverage
rm -rf build dist

echo "[INFO] Cleaned environment"