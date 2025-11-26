# User Display Optimizer

Fast, cross-platform user display utilities with one-command setup, tests, and Docker support.

## Quick Start

### Linux/macOS
```bash
bash setup.sh      # create .venv & install deps
bash run.sh        # run optimized module with timing
bash test.sh       # pytest + coverage
bash clean.sh      # remove venv/artifacts
```

### Windows PowerShell
```powershell
powershell -File setup.ps1
powershell -File run.ps1
powershell -File test.ps1
powershell -File clean.ps1
```

### Docker
```bash
docker build -t user-display-optimizer .
docker run --rm user-display-optimizer              # runs tests
docker run --rm user-display-optimizer bash run.sh   # optional timing demo
```

## Project Structure
```
.
├── user_display_original.py       # Original reference (inefficient)
├── user_display_optimized.py      # Optimized implementation
├── requirements.txt               # pytest + pytest-cov
├── setup.sh / setup.ps1           # Create venv, install deps
├── run.sh / run.ps1               # Run optimized module with timing
├── test.sh / test.ps1             # Run tests with coverage
├── clean.sh / clean.ps1           # Clean artifacts
├── Dockerfile / .dockerignore     # Container support
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_user_display.py
```

## Before vs After

| Area | Original | Optimized |
|------|----------|-----------|
| String building | `+=` in loop (O(n²)) | List accumulation + `"\n".join()` |
| Delays | `time.sleep(0.01)` per user | No artificial delays |
| Lookup | Linear search | Optional prebuilt index (O(1)) |
| Filtering | Nested conditionals | Clear logic with logging |
| Error handling | None (KeyError) | Graceful logging `[MARKER]` |
| Logging | Print statements | Structured `logging` |
| Tests | None | Pytest + coverage (>85%) |
| Cross-platform | Unspecified | Bash + PowerShell + Docker |

## Performance Targets

- `display_users(100)` < **50 ms**
- `display_users(1000)` < **100 ms**
- `filter_users(100)` < **10 ms**
- `get_user_by_id` O(1) with prebuilt index

Tests enforce timing with generous buffer to avoid flakiness.

## Implementation Highlights

- `user_display_optimized.py` uses:
  - `TypedDict` for user records
  - Efficient joins for string building
  - `build_user_index()` for O(1) lookups
  - Graceful KeyError handling with `[DISPLAY]`, `[FILTER]`, `[GET]`, `[EXPORT]` markers
  - Optional verbose/debug logging
- Helper `generate_sample_users(n)` for demos/tests

## Coverage

```bash
pytest --cov=user_display_optimized --cov-report=term-missing
```

## Notes

- Requires Python **3.10+**.
- Scripts are idempotent; rerunning `setup` is safe.
- No hardcoded paths; works on Windows, macOS, Linux.
