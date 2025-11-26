#!/bin/bash
# clean.sh - Clean up environment on macOS/Linux

set -e

echo -e "\033[32mCleaning up environment...\033[0m"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Remove virtual environment
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo -e "\033[33mRemoving virtual environment...\033[0m"
    rm -rf "$SCRIPT_DIR/venv"
    echo -e "\033[32mVirtual environment removed\033[0m"
else
    echo -e "\033[33mVirtual environment not found, skipping...\033[0m"
fi

# Remove __pycache__ directories
echo -e "\033[33mRemoving __pycache__ directories...\033[0m"
find "$SCRIPT_DIR" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Remove .pytest_cache
if [ -d "$SCRIPT_DIR/.pytest_cache" ]; then
    echo -e "\033[33mRemoving .pytest_cache...\033[0m"
    rm -rf "$SCRIPT_DIR/.pytest_cache"
fi

# Remove htmlcov
if [ -d "$SCRIPT_DIR/htmlcov" ]; then
    echo -e "\033[33mRemoving htmlcov directory...\033[0m"
    rm -rf "$SCRIPT_DIR/htmlcov"
fi

# Remove .coverage
if [ -f "$SCRIPT_DIR/.coverage" ]; then
    echo -e "\033[33mRemoving .coverage file...\033[0m"
    rm -f "$SCRIPT_DIR/.coverage"
fi

# Remove .egg-info directories
find "$SCRIPT_DIR" -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

echo -e "\n\033[32mCleanup completed successfully!\033[0m"
exit 0
