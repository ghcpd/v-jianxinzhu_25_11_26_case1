#!/bin/bash
# Test script - Run tests with coverage
# Works on Linux/macOS

set -e

echo "================================================"
echo "Running Tests with Coverage"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run: bash setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run tests with coverage
echo "Running pytest with coverage..."
echo ""
pytest tests/ -v --cov=user_display_optimized --cov-report=term-missing --cov-report=html

echo ""
echo "================================================"
echo "Tests complete!"
echo "================================================"
echo "Coverage report saved to htmlcov/index.html"
echo "================================================"

exit 0
