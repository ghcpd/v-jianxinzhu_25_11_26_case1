# User Display Optimizer

This project refactors an inefficient user display module into a high-performance, cross-platform, and well-tested package.

Quick start (bash):

    bash setup.sh
    bash test.sh
    bash run.sh
    bash clean.sh

PowerShell (Windows):

    powershell -File setup.ps1
    powershell -File test.ps1
    powershell -File run.ps1
    powershell -File clean.ps1

Docker:

    docker build -t user-display-optimizer .
    docker run --rm user-display-optimizer

What's included:

- `user_display_original.py`: original implementation preserved
- `user_display_optimized.py`: optimized, typed, and logged implementation
- `tests/`: pytest test suite with >85% coverage
- `Dockerfile`: CI-friendly container for running tests

Key improvements:

- O(1) get_user_by_id via indexing
- Efficient string building (join) instead of repeated concatenation
- No artificial delays
- Graceful error handling and structured logging

Performance goals:

- Display 100 users in <50ms
- Display 1000 users in <100ms

