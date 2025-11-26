# User Display Optimizer

This repository contains an optimized implementation of a `user_display` code sample. It is designed to be fast, maintainable, and cross-platform.

## Quickstart

On macOS / Linux:

```bash
./setup.sh       # Create venv and install deps
./run.sh         # Run the optimized module (shows times & sample output)
./test.sh        # Run tests and coverage (will fail if coverage < 85%)
./clean.sh       # Remove venv and caches
```

On Windows (PowerShell):

```powershell
powershell -File .\setup.ps1
powershell -File .\run.ps1
powershell -File .\test.ps1
powershell -File .\clean.ps1
```

## Files

- `user_display_original.py` — preserved original for reference
- `user_display_optimized.py` — optimized, type-hinted, logging, tested
- `tests/` — pytest tests and fixtures
- `setup.sh/setup.ps1` — idempotent setup scripts
- `run.sh/run.ps1` — run optimized module
- `test.sh/test.ps1` — run pytest with coverage (enforces 85%)
- `clean.sh/clean.ps1` — clean build artifacts and venv
- `Dockerfile` — container image runs tests and enforces coverage

## Before / After

- Old implementation used repeated string concatenation in loops and a linear lookup by ID.
- Optimized implementation uses list accumulation and `join()`, builds an index for `O(1)` lookups, and simplifies filtering using comprehensions.

## Performance Targets

- Display 100 users: <50ms
- Display 1000 users: <100ms
- Filter 100 users: <10ms
- Get user by ID: <1ms

These are enforced by tests in `tests/test_user_display.py`.

## Docker

Build and test:

```bash
docker build -t user-display-optimizer .
docker run --rm user-display-optimizer
```

Run in docker and execute the module:

```bash
docker run --rm user-display-optimizer bash -lc "python user_display_optimized.py"
```
