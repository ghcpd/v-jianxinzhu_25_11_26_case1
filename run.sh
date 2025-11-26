#!/bin/bash
# run.sh - Run optimized user display module with timing on macOS/Linux

set -e

MODULE="${1:-user_display_optimized}"

echo -e "\033[32mRunning optimized user display module...\033[0m"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if venv exists
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    echo -e "\033[33mActivating virtual environment...\033[0m"
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo -e "\033[33mWARNING: Virtual environment not found. Using system Python...\033[0m"
fi

# Run with timing
echo -e "\033[33mExecution started at: $(date '+%Y-%m-%d %H:%M:%S.%3N')\033[0m"

START_TIME=$(date +%s%N)

python "$SCRIPT_DIR/$MODULE.py"

END_TIME=$(date +%s%N)
ELAPSED_MS=$(( ($END_TIME - $START_TIME) / 1000000 ))

echo -e "\n\033[32m========================================\033[0m"
echo -e "\033[33mExecution completed at: $(date '+%Y-%m-%d %H:%M:%S.%3N')\033[0m"
echo -e "\033[33mTotal execution time: ${ELAPSED_MS}ms\033[0m"
echo -e "\033[32m========================================\033[0m"

exit 0
