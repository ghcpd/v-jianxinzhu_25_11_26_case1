#!/bin/bash
# Run script - Execute the optimized module
# Works on Linux/macOS

set -e

echo "================================================"
echo "Running User Display Optimizer"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run: bash setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the optimized module
echo "Executing user_display_optimized.py..."
echo ""
python user_display_optimized.py

echo ""
echo "================================================"
echo "Execution complete!"
echo "================================================"

exit 0
