#!/bin/bash
# setup.sh - Setup virtual environment and install dependencies on macOS/Linux

set -e

echo -e "\033[32mSetting up Python environment...\033[0m"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "\033[31mERROR: Python3 is not installed or not in PATH\033[0m"
    exit 1
fi

PYTHON_EXE=$(command -v python3)
echo -e "\033[33mPython executable: $PYTHON_EXE\033[0m"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if venv already exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo -e "\033[33mVirtual environment already exists. Skipping venv creation...\033[0m"
else
    echo -e "\033[33mCreating virtual environment...\033[0m"
    python3 -m venv "$SCRIPT_DIR/venv"
    
    if [ $? -ne 0 ]; then
        echo -e "\033[31mERROR: Failed to create virtual environment\033[0m"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "\033[33mActivating virtual environment...\033[0m"
source "$SCRIPT_DIR/venv/bin/activate"

# Upgrade pip
echo -e "\033[33mUpgrading pip...\033[0m"
python -m pip install --upgrade pip

if [ $? -ne 0 ]; then
    echo -e "\033[33mWARNING: pip upgrade encountered issues but continuing...\033[0m"
fi

# Install requirements
echo -e "\033[33mInstalling dependencies from requirements.txt...\033[0m"
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip install -r "$SCRIPT_DIR/requirements.txt"
    
    if [ $? -ne 0 ]; then
        echo -e "\033[31mERROR: Failed to install requirements\033[0m"
        exit 1
    fi
else
    echo -e "\033[31mERROR: requirements.txt not found\033[0m"
    exit 1
fi

echo -e "\n\033[32mSetup completed successfully!\033[0m"
echo -e "\033[33mVirtual environment is at: $SCRIPT_DIR/venv\033[0m"
echo -e "\033[33mTo activate manually, run: source $SCRIPT_DIR/venv/bin/activate\033[0m"
exit 0
