#!/bin/bash
# Clean script - Remove virtual environment and generated files
# Works on Linux/macOS

set -e

echo "================================================"
echo "Cleaning Environment"
echo "================================================"

# Remove virtual environment
if [ -d "venv" ]; then
    echo "Removing virtual environment..."
    rm -rf venv
fi

# Remove pytest cache
if [ -d ".pytest_cache" ]; then
    echo "Removing pytest cache..."
    rm -rf .pytest_cache
fi

# Remove coverage files
if [ -d "htmlcov" ]; then
    echo "Removing coverage reports..."
    rm -rf htmlcov
fi

if [ -f ".coverage" ]; then
    rm -f .coverage
fi

# Remove Python cache
if [ -d "__pycache__" ]; then
    echo "Removing Python cache..."
    rm -rf __pycache__
fi

if [ -d "tests/__pycache__" ]; then
    rm -rf tests/__pycache__
fi

echo ""
echo "================================================"
echo "Cleanup complete!"
echo "================================================"
echo "To set up again, run:"
echo "  bash setup.sh"
echo "================================================"

exit 0
