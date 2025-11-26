"""Optimized user display utilities.

Goals and features:
- Efficient operations (O(1) lookups using an index)
- Minimal memory churn (joins instead of +=)
- No artificial delays, fast bulk operations
- Type hints, docstrings, and structured logging
- Graceful error handling; missing keys handled with defaults

This module is cross-platform and has no external dependencies.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional
import logging
import time

LOGGER_NAME = "user_display"
_logger = logging.getLogger(LOGGER_NAME)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the module logger with a simple console handler.

    The function is idempotent so it is safe to call from scripts/tests.
    """
    if _logger.handlers:
        _logger.setLevel(level)
        return

    handler = logging.StreamHandler()
    fmt = "[MARKER] %(levelname)s:%(name)s: %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    _logger.addHandler(handler)
    _logger.setLevel(level)


def _safe_get(user: Mapping[str, Any], key: str, default: str = "N/A") -> str:
    """Fetch a value from a user mapping and return a safe string.

    This keeps the public functions resilient when fields are missing.
    """
    try:
        value = user.get(key, default)  # type: ignore[attr-defined]
    except Exception:  # defensive: if user isn't a mapping
        _logger.warning("Missing/invalid user object when reading %s", key)
        return default
    if value is None:
        return default
    return str(value)


def display_users(users: Iterable[Mapping[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """Return a compact multi-line display string for `users`.

    - Uses a list + join strategy (O(n) allocation, no repeated concatenation)
    - Handles missing keys gracefully and logs at marker level

    Args:
        users: Iterable of mappings containing user fields
        show_all: If True, append a summary line
        verbose: If True, emit per-item debug messages

    Returns:
        A multi-line string.
    """
    lines: List[str] = []
    count = 0

    for user in users:
        if verbose:
            _logger.info("Processing user %s", _safe_get(user, "id"))
        uid = _safe_get(user, "id")
        name = _safe_get(user, "name")
        email = _safe_get(user, "email")
        role = _safe_get(user, "role")
        status = _safe_get(user, "status")
        join_date = _safe_get(user, "join_date")
        last_login = _safe_get(user, "last_login")

        lines.append(
            "|".join([
                f"ID:{uid}",
                f"Name:{name}",
                f"Email:{email}",
                f"Role:{role}",
                f"Status:{status}",
                f"JoinDate:{join_date}",
                f"LastLogin:{last_login}",
            ])
        )
        count += 1

    if show_all:
        lines.append(f"[INFO] Processed {count} users.")

    return "\n".join(lines) + ("\n" if lines else "")


def build_user_index(users: Iterable[Mapping[str, Any]]) -> Dict[Any, Mapping[str, Any]]:
    """Build an index map from user id to user mapping for O(1) lookup.

    If duplicate IDs are present the first occurrence wins and a marker is logged.
    """
    index: Dict[Any, Mapping[str, Any]] = {}
    for user in users:
        try:
            uid = user["id"]
        except Exception:
            _logger.warning("Skipping user with missing 'id' field: %r", user)
            continue
        if uid in index:
            _logger.warning("Duplicate id %r encountered; ignoring subsequent entry", uid)
            continue
        index[uid] = user
    return index


def get_user_by_id(users: Iterable[Mapping[str, Any]], user_id: Any) -> Optional[Mapping[str, Any]]:
    """Get a user by id in O(1) time by building a small index.

    This function is intentionally light-weight: it will build a short-lived index
    if the caller passes an iterable. For heavy workloads, callers should call
    `build_user_index` and reuse it.
    """
    idx = build_user_index(users)
    return idx.get(user_id)


def filter_users(users: Iterable[Mapping[str, Any]], **criteria: Any) -> List[Mapping[str, Any]]:
    """Filter users by simple criteria.

    Accepts keyword criteria: role, status, name. name performs case-insensitive substring match.

    Implemented using list comprehension for readability and speed.
    """
    def match(u: Mapping[str, Any]) -> bool:
        if "role" in criteria and str(u.get("role", "")).lower() != str(criteria["role"]).lower():
            return False
        if "status" in criteria and str(u.get("status", "")).lower() != str(criteria["status"]).lower():
            return False
        if "name" in criteria and str(criteria["name"]).lower() not in str(u.get("name", "")).lower():
            return False
        return True

    return [u for u in users if match(u)]


def export_users_to_string(users: Iterable[Mapping[str, Any]]) -> str:
    """Export users into a human-readable multi-line string efficiently.

    Uses join operations and handles missing keys gracefully.
    """
    header = ["USER_EXPORT_START", "=" * 80]
    body_lines: List[str] = []
    for user in users:
        uid = _safe_get(user, "id")
        body_lines.extend([
            f"User ID: {uid}",
            f"  Name: {_safe_get(user, 'name')}",
            f"  Email: {_safe_get(user, 'email')}",
            f"  Role: {_safe_get(user, 'role')}",
            f"  Status: {_safe_get(user, 'status')}",
            f"  Join Date: {_safe_get(user, 'join_date')}",
            f"  Last Login: {_safe_get(user, 'last_login')}",
            "-" * 80,
        ])

    tail = ["USER_EXPORT_END"]
    parts = header + body_lines + tail
    return "\n".join(parts) + "\n"


def measure_execution_ms(callable_obj, *args, **kwargs) -> float:
    """Measure a callable and return elapsed time in milliseconds."""
    start = time.perf_counter()
    callable_obj(*args, **kwargs)
    end = time.perf_counter()
    return (end - start) * 1000.0


__all__ = [
    "display_users",
    "get_user_by_id",
    "filter_users",
    "export_users_to_string",
    "build_user_index",
    "configure_logging",
    "measure_execution_ms",
]


if __name__ == "__main__":
    configure_logging()

    # Small sample demonstration
    sample_users = [
        {"id": i, "name": f"User {i}", "email": f"user{i}@example.com", "role": "User", "status": "Active", "join_date": "2024-01-01", "last_login": "2025-11-26"}
        for i in range(1, 6)
    ]

    print("Optimized Implementation (sample):")
    print("=" * 100)
    print(display_users(sample_users))

    # Quick performance sanity check
    large = [
        {"id": i, "name": f"User {i}", "email": f"user{i}@example.com", "role": "User", "status": "Active", "join_date": "2024-01-01", "last_login": "2025-11-26"}
        for i in range(1, 1001)
    ]
    t_ms = measure_execution_ms(display_users, large)
    _logger.info("Displaying 1000 users took %.2fms", t_ms)
