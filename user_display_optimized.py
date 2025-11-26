"""Optimized user display implementation.

Features:
- Type hints, docstrings, PEP8
- Logging with markers
- No artificial delays
- O(1) get_user_by_id via index
- Efficient string building using join
- Graceful error handling
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional
import logging
import time

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

MARKER = "[USER-DISPLAY]"


def _safe_get(user: Dict[str, Any], key: str) -> Any:
    """Return a safe value for a user key, logging missing keys.

    This ensures missing keys don't raise KeyError in display/export functions.
    """
    if key not in user:
        logger.warning("%s Missing key '%s' in user %s", MARKER, key, user.get("id", "<unknown>"))
        return "<missing>"
    return user[key]


def build_user_index(users: Iterable[Dict[str, Any]]) -> Dict[Any, Dict[str, Any]]:
    """Create an index mapping user id -> user dict for O(1) lookups.

    Args:
        users: Iterable of user dicts.
    Returns:
        dict: {id: user}
    """
    index: Dict[Any, Dict[str, Any]] = {}
    for u in users:
        uid = u.get("id")
        if uid is None:
            logger.warning("%s Skipping user without id: %s", MARKER, u)
            continue
        index[uid] = u
    logger.debug("%s Built index for %d users", MARKER, len(index))
    return index


def display_users(users: Iterable[Dict[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """Return a compact string representing users in a fast, safe, and readable manner.

    This uses list-join for efficient string building and handles missing keys gracefully.
    """
    start = time.perf_counter()
    lines: List[str] = []
    processed_count = 0

    for user in users:
        if verbose:
            logger.debug("%s Processing user %s", MARKER, user.get("id"))
        uid = _safe_get(user, "id")
        name = _safe_get(user, "name")
        email = _safe_get(user, "email")
        role = _safe_get(user, "role")
        status = _safe_get(user, "status")
        join_date = _safe_get(user, "join_date")
        last_login = _safe_get(user, "last_login")

        # Single formatted string per user and store in list
        line = (
            f"ID:{uid}|Name:{name}|Email:{email}|Role:{role}|Status:{status}|"
            f"JoinDate:{join_date}|LastLogin:{last_login}"
        )
        lines.append(line)
        processed_count += 1

    if show_all:
        lines.append(f"[INFO] Processed {processed_count} users.")

    result = "\n".join(lines) + ("\n" if lines else "")
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("%s display_users completed in %.2fms for %d users", MARKER, elapsed_ms, processed_count)
    return result


def get_user_by_id(users: Iterable[Dict[str, Any]], user_id: Any, index: Optional[Dict[Any, Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    """Get user by ID using an index for O(1) lookup. If no index is provided,
    one will be created temporarily.

    Args:
        users: Iterable of user dicts
        user_id: ID to lookup
        index: Optional index to use (id -> user dict)
    Returns:
        the user dict or None
    """
    if index is None:
        index = build_user_index(users)
    user = index.get(user_id)
    if user is None:
        logger.info("%s get_user_by_id: id=%s not found", MARKER, user_id)
    else:
        logger.debug("%s get_user_by_id: found id=%s", MARKER, user_id)
    return user


def filter_users(users: Iterable[Dict[str, Any]], criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Filter users quickly using list comprehensions and simple predicate checks.

    Supported criteria keys: name (substring, case-insensitive), role, status.
    """
    users_list = list(users)
    if not criteria:
        return users_list

    role = criteria.get("role")
    status = criteria.get("status")
    name = criteria.get("name")

    def matches(u: Dict[str, Any]) -> bool:
        try:
            if role and u.get("role") != role:
                return False
            if status and u.get("status") != status:
                return False
            if name and name.lower() not in (u.get("name") or "").lower():
                return False
            return True
        except Exception:
            logger.exception("%s Error while filtering user: %s", MARKER, u)
            return False

    filtered = [u for u in users_list if matches(u)]
    logger.info("%s filter_users: %d -> %d after filtering", MARKER, len(users_list), len(filtered))
    return filtered


def export_users_to_string(users: Iterable[Dict[str, Any]]) -> str:
    """Export users to a human-readable string efficiently using join.

    Uses safe getters to avoid KeyError and logs missing keys.
    """
    parts: List[str] = ["USER_EXPORT_START", "=" * 100]
    for u in users:
        uid = _safe_get(u, "id")
        parts.append(f"User ID: {uid}")
        parts.append(f"  Name: {_safe_get(u, 'name')}")
        parts.append(f"  Email: {_safe_get(u, 'email')}")
        parts.append(f"  Role: {_safe_get(u, 'role')}")
        parts.append(f"  Status: {_safe_get(u, 'status')}")
        parts.append(f"  Join Date: {_safe_get(u, 'join_date')}")
        parts.append(f"  Last Login: {_safe_get(u, 'last_login')}")
        parts.append("-" * 100)
    parts.append("USER_EXPORT_END")
    result = "\n".join(parts) + "\n"
    logger.info("%s export_users_to_string: %d users", MARKER, len(parts) // 9)
    return result


if __name__ == "__main__":
    # Demo run with logging to console
    logging.basicConfig(level=logging.INFO)
    from time import perf_counter

    sample_users = [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'Admin',
            'status': 'Active',
            'join_date': '2023-01-15',
            'last_login': '2025-11-26'
        },
    ]
    start = perf_counter()
    print(display_users(sample_users, verbose=True))
    print(export_users_to_string(sample_users))
    print(get_user_by_id(sample_users, 1))
    print("Elapsed: %.2fms" % ((perf_counter() - start) * 1000))
