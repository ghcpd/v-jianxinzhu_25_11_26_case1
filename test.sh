#!/bin/bash
# test.sh - Run tests with coverage on macOS/Linux

set -e

COVERAGE=false
MIN_COVERAGE=85

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage)
            COVERAGE=true
            shift
            ;;
        --min-coverage)
            MIN_COVERAGE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "\033[32mRunning test suite...\033[0m"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if venv exists
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    echo -e "\033[33mActivating virtual environment...\033[0m"
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo -e "\033[33mWARNING: Virtual environment not found. Using system Python...\033[0m"
fi

# Build pytest arguments
PYTEST_ARGS=(
    "$SCRIPT_DIR/tests"
    "-v"
    "--tb=short"
)

# Add coverage if requested
if [ "$COVERAGE" = true ]; then
    PYTEST_ARGS+=(
        "--cov=$SCRIPT_DIR/user_display_optimized"
        "--cov-report=term-missing"
        "--cov-report=html:$SCRIPT_DIR/htmlcov"
        "--cov-fail-under=$MIN_COVERAGE"
    )
    echo -e "\033[33mRunning with coverage (minimum $MIN_COVERAGE%)...\033[0m"
else
    echo -e "\033[33mRunning without coverage...\033[0m"
fi

# Run tests
echo -e "\033[33mExecution started at: $(date '+%Y-%m-%d %H:%M:%S.%3N')\033[0m"

START_TIME=$(date +%s%N)

pytest "${PYTEST_ARGS[@]}"
TEST_EXIT_CODE=$?

END_TIME=$(date +%s%N)
ELAPSED_MS=$(( ($END_TIME - $START_TIME) / 1000000 ))

echo -e "\n\033[32m========================================\033[0m"
echo -e "\033[33mTest execution completed at: $(date '+%Y-%m-%d %H:%M:%S.%3N')\033[0m"
echo -e "\033[33mTotal execution time: ${ELAPSED_MS}ms\033[0m"
echo -e "\033[32m========================================\033[0m"

if [ "$COVERAGE" = true ]; then
    echo -e "\033[33mHTML coverage report generated at: $SCRIPT_DIR/htmlcov/index.html\033[0m"
fi

exit $TEST_EXIT_CODE
