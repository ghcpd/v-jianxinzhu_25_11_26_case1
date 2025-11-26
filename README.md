# User Display Optimizer — Cross-platform, fast, and testable

This repository refactors a naive user display utility into a fast, well-tested, cross-platform package. Everything is designed to run on Windows, macOS, or Linux and in Docker.

Key files:

- `user_display_original.py` — Original (reference) implementation preserved.
- `user_display_optimized.py` — Refactored, type-hinted, logged, and performance-focused implementation.
- `tests/` — Pytest test suite with performance & logging checks.
- `requirements.txt` — Minimal pinned deps for tests
- `setup.sh` / `setup.ps1` — Idempotent environment setup (venv + deps)
- `run.sh` / `run.ps1` — Run the optimized module
- `test.sh` / `test.ps1` — Run tests + coverage (fail if coverage < 85%)
- `clean.sh` / `clean.ps1` — Remove venv and caches
- `Dockerfile` / `.dockerignore` — Build a container and run tests

Quick start (Linux/macOS):

```bash
bash setup.sh    # create .venv and install pinned deps
bash run.sh      # run the optimized module demo
bash test.sh     # run tests with coverage (fails if <85%)
bash clean.sh    # cleanup environment
```

Quick start (Windows PowerShell):

```powershell
powershell -File setup.ps1
powershell -File run.ps1
powershell -File test.ps1
powershell -File clean.ps1
```

Docker

```bash
docker build -t user-display-optimizer .
docker run --rm user-display-optimizer
docker run --rm user-display-optimizer bash -lc "python -m user_display_optimized"
```

Before vs After

The original code used repeated string concatenation in loops, introduced artificial delays using sleep, performed linear searches for lookups, and lacked defensive error handling and logging.

The optimized version:

- Uses list comprehension and join to avoid O(n^2) string operations
- Builds an index for O(1) id lookups
- Removes artificial sleeps and unnecessary allocations
- Adds type hints, docstrings, logging ("[MARKER]") and defensive handling for missing keys
- Well-covered tests and scripts for reproducible cross-platform execution

Performance targets (validated by tests):

| Operation | Target |
|---|---:|
| Display 100 users | < 50 ms |
| Display 1000 users | < 100 ms |
| Filter 100 users | < 10 ms |
| Get user by ID | < 1 ms |

If you want any CI integration (GitHub Actions) or packaging help, I can add those too.
