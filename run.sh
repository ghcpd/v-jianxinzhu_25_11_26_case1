#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
source .venv/bin/activate

python - <<'PYCODE'
from user_display_optimized import generate_sample_users, display_users
import time

users = generate_sample_users(1000)
start = time.perf_counter()
display_users(users, show_all=False)
elapsed_ms = (time.perf_counter() - start) * 1000
print(f"display_users(1000) took {elapsed_ms:.2f} ms")
PYCODE
