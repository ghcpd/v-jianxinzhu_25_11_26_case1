"""Optimized user display utilities.

- Fast string building via joins
- Optional O(1) user lookup using prebuilt index
- Simplified filtering logic
- Graceful error handling with logging markers
- Type hints and PEP 8 compliance
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, TypedDict

__all__ = [
    "User",
    "UserIndex",
    "display_users",
    "get_user_by_id",
    "filter_users",
    "export_users_to_string",
    "build_user_index",
    "generate_sample_users",
]


class User(TypedDict, total=False):
    """Typed representation of a user record.

    Keys are optional to allow graceful handling of incomplete records.
    """

    id: int
    name: str
    email: str
    role: str
    status: str
    join_date: str
    last_login: str


UserIndex = Dict[Any, User]

LOGGER_NAME = "user_display"
logger = logging.getLogger(LOGGER_NAME)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure module logger with a simple stream handler if not already configured."""

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)


# Ensure default logging is configured for scripts that run this module directly.
configure_logging()


def build_user_index(users: Iterable[User]) -> UserIndex:
    """Build an index mapping user IDs to user records.

    Missing ``id`` keys are skipped and logged.
    """

    index: UserIndex = {}
    for user in users:
        try:
            uid = user["id"]  # type: ignore[index]
        except KeyError:
            logger.warning("[GET][ERROR] Missing 'id' in user record; skipping: %s", user)
            continue
        index[uid] = user
    logger.debug("[GET] Built user index of size %d", len(index))
    return index


def _safe_get(user: User, key: str) -> Optional[Any]:
    try:
        return user[key]
    except KeyError:
        logger.error("[DISPLAY][ERROR] Missing key '%s' in user: %s", key, user)
        return None


def display_users(
    users: Sequence[User],
    show_all: bool = True,
    verbose: bool = False,
) -> str:
    """Return a compact string representation of users.

    - Uses list accumulation + ``"\n".join`` for speed.
    - Logs and skips users with missing fields.
    - When ``verbose`` is True, logs per-user processing at DEBUG level.
    """

    logger.info("[DISPLAY] Rendering %d users", len(users))

    lines: List[str] = []
    for user in users:
        if verbose:
            logger.debug("[DISPLAY] Processing user %s", user.get("id", "<unknown>"))

        id_ = _safe_get(user, "id")
        name = _safe_get(user, "name")
        email = _safe_get(user, "email")
        role = _safe_get(user, "role")
        status = _safe_get(user, "status")
        join_date = _safe_get(user, "join_date")
        last_login = _safe_get(user, "last_login")

        if None in (id_, name, email, role, status, join_date, last_login):
            continue

        line = (
            f"ID:{id_}|Name:{name}|Email:{email}|Role:{role}|"
            f"Status:{status}|JoinDate:{join_date}|LastLogin:{last_login}"
        )
        lines.append(line)

    if show_all:
        lines.append(f"[INFO] Processed {len(lines)} users.")

    logger.info("[DISPLAY] Processed %d valid users", len(lines) - (1 if show_all else 0))

    return "\n".join(lines) + ("\n" if lines else "")


def get_user_by_id(
    users: Sequence[User] | Mapping[Any, User],
    user_id: Any,
    user_index: Optional[Mapping[Any, User]] = None,
) -> Optional[User]:
    """Retrieve a user by ``user_id`` in O(1) using a prebuilt index.

    Pass a ``user_index`` (from :func:`build_user_index`) for best performance.
    If ``users`` is already a mapping, it's used directly.
    """

    if user_index is not None:
        return user_index.get(user_id)  # type: ignore[return-value]

    if isinstance(users, Mapping):
        return users.get(user_id)  # type: ignore[return-value]

    # Fallback: build a small index (still O(n) once). For repeated lookups, caller
    # should prebuild via ``build_user_index`` and pass it in.
    index = build_user_index(users)
    return index.get(user_id)


def filter_users(users: Sequence[User], criteria: Mapping[str, Any]) -> List[User]:
    """Filter users by criteria.

    Supported keys: ``role``, ``status``, ``name`` (substring, case-insensitive).
    Missing keys in user records are logged and skipped.
    """

    if not criteria:
        logger.debug("[FILTER] No criteria provided; returning all users (%d)", len(users))
        return list(users)

    logger.info("[FILTER] Applying criteria: %s", criteria)
    filtered: List[User] = []
    for user in users:
        try:
            matches_role = criteria.get("role") is None or user.get("role") == criteria.get("role")
            matches_status = criteria.get("status") is None or user.get("status") == criteria.get("status")
            name_crit = criteria.get("name")
            user_name = user.get("name")
            matches_name = True
            if name_crit is not None:
                if user_name is None:
                    raise KeyError("name")
                matches_name = name_crit.lower() in user_name.lower()
        except KeyError as exc:
            logger.error("[FILTER][ERROR] Missing key %s in user: %s", exc, user)
            continue

        if matches_role and matches_status and matches_name:
            filtered.append(user)

    logger.info("[FILTER] Matched %d users", len(filtered))
    return filtered


def export_users_to_string(users: Sequence[User]) -> str:
    """Export users to a formatted string efficiently.

    Skips users with missing required fields and logs errors.
    """

    logger.info("[EXPORT] Exporting %d users", len(users))

    lines: List[str] = ["USER_EXPORT_START", "=" * 100]
    for user in users:
        id_ = _safe_get(user, "id")
        name = _safe_get(user, "name")
        email = _safe_get(user, "email")
        role = _safe_get(user, "role")
        status = _safe_get(user, "status")
        join_date = _safe_get(user, "join_date")
        last_login = _safe_get(user, "last_login")

        if None in (id_, name, email, role, status, join_date, last_login):
            continue

        lines.extend(
            [
                f"User ID: {id_}",
                f"  Name: {name}",
                f"  Email: {email}",
                f"  Role: {role}",
                f"  Status: {status}",
                f"  Join Date: {join_date}",
                f"  Last Login: {last_login}",
                "-" * 100,
            ]
        )

    lines.append("USER_EXPORT_END")
    logger.info("[EXPORT] Exported %d users", (len(lines) - 3) // 8)
    return "\n".join(lines) + "\n"


def generate_sample_users(n: int) -> List[User]:
    """Generate a list of sample users for demos/tests."""

    return [
        {
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "role": "Admin" if i % 5 == 0 else "User",
            "status": "Active" if i % 3 != 0 else "Inactive",
            "join_date": f"2023-01-{(i % 28) + 1:02d}",
            "last_login": f"2025-11-{(i % 28) + 1:02d}",
        }
        for i in range(1, n + 1)
    ]


def _demo() -> None:
    users = generate_sample_users(5)
    start = time.perf_counter()
    output = display_users(users)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("[DISPLAY] Completed in %.2f ms", elapsed_ms)
    print(output)


if __name__ == "__main__":
    _demo()
