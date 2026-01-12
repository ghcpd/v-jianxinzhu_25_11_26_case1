#!/bin/bash
# Setup script - Create virtual environment and install dependencies
# Works on Linux/macOS

set -e

echo "================================================"
echo "Setting up User Display Optimizer Environment"
echo "================================================"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "================================================"
echo "Setup complete!"
echo "================================================"
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests, use:"
echo "  bash test.sh"
echo ""
echo "To run the optimized module, use:"
echo "  bash run.sh"
echo "================================================"

exit 0
