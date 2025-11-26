"""Optimized user display module.

Features:
- Fast display with list joins (no string concatenation in loops)
- O(1) get_user_by_id via index
- Simple list-comprehension based filter
- Export optimized to reduce memory churn
- Type hints, logging, error handling
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional
import logging
import time

LOG_FORMAT = "[MARKER] %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


User = Dict[str, Any]


@dataclass
class UserManager:
    """Container for users with an index for quick lookups.

    The class stores original list and builds an index mapping `id` to user
    so `get_user_by_id` is O(1).
    """

    users: List[User] = field(default_factory=list)
    _index_by_id: Dict[Any, User] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        logger.info("[MARKER] Building index for %s users", len(self.users))
        # Build index; last wins for duplicate IDs.
        for u in self.users:
            try:
                uid = u.get('id')
                if uid is not None:
                    self._index_by_id[uid] = u
            except Exception as exc:  # robustly handle malformed entries
                logger.warning("[MARKER] Skipping malformed user during index build: %s", exc)

    def get_user_by_id(self, user_id: Any) -> Optional[User]:
        """Return user by id in O(1) time.

        Returns None if missing.
        """
        logger.info("[MARKER] Lookup user id=%s", user_id)
        return self._index_by_id.get(user_id)

    def filter_users(self, role: Optional[str] = None, status: Optional[str] = None, name: Optional[str] = None) -> List[User]:
        """Filter users by provided criteria using list comprehensions.

        Only provided criteria are applied.
        """
        logger.info("[MARKER] Filtering users role=%s status=%s name=%s", role, status, name)

        def predicate(u: User) -> bool:
            if role and u.get('role') != role:
                return False
            if status and u.get('status') != status:
                return False
            if name and name.lower() not in (u.get('name') or '').lower():
                return False
            return True

        return [u for u in self.users if predicate(u)]

    def display_users(self, show_all: bool = True, verbose: bool = False) -> str:
        """Return a multi-line display string for users.

        Efficiently builds lines and uses .join() for fast concatenation.
        """
        lines: List[str] = []
        processed_count = 0
        for u in self.users:
            if verbose:
                logger.info("[MARKER] Processing user %s", u.get('id'))
            # Use .get with default to avoid KeyError
            try:
                user_id = u.get('id', 'N/A')
                name = u.get('name', 'N/A')
                email = u.get('email', 'N/A')
                role = u.get('role', 'N/A')
                status = u.get('status', 'N/A')
                join_date = u.get('join_date', 'N/A')
                last_login = u.get('last_login', 'N/A')

                line = (
                    f"ID:{user_id}|Name:{name}|Email:{email}|Role:{role}|"
                    f"Status:{status}|JoinDate:{join_date}|LastLogin:{last_login}"
                )
                lines.append(line)
                processed_count += 1
            except Exception as exc:
                # Non-fatal: log and continue
                logger.exception("[MARKER] Error formatting user: %s", exc)
                continue

        if show_all:
            lines.append(f"\n[INFO] Processed {processed_count} users.")
        return "\n".join(lines)

    def export_users_to_string(self) -> str:
        """Export users to a single string efficiently.

        Uses list accumulation and join, reduces temporary string churn.
        """
        logger.info("[MARKER] Exporting %s users", len(self.users))
        lines: List[str] = ["USER_EXPORT_START", "=" * 100]
        for u in self.users:
            uid = u.get('id', 'N/A')
            lines.extend([
                f"User ID: {uid}",
                f"  Name: {u.get('name', 'N/A')}",
                f"  Email: {u.get('email', 'N/A')}",
                f"  Role: {u.get('role', 'N/A')}",
                f"  Status: {u.get('status', 'N/A')}",
                f"  Join Date: {u.get('join_date', 'N/A')}",
                f"  Last Login: {u.get('last_login', 'N/A')}",
                "-" * 100,
            ])
        lines.append("USER_EXPORT_END")
        return "\n".join(lines)


def _build_sample_users(n: int = 5) -> List[User]:
    """Builds a short list of sample users for manual testing/run.

    The IDs start at 1.
    """
    out = []
    for i in range(1, n + 1):
        out.append(
            {
                'id': i,
                'name': f'User {i}',
                'email': f'user{i}@example.com',
                'role': 'User' if i % 3 else 'Admin',
                'status': 'Active' if i % 2 else 'Inactive',
                'join_date': '2024-01-01',
                'last_login': '2025-11-26',
            }
        )
    return out


def main() -> int:
    sample_users = _build_sample_users(1000)
    manager = UserManager(sample_users)

    # Timed operations
    t0 = time.perf_counter()
    _ = manager.display_users(show_all=False)
    t_display = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    _ = manager.get_user_by_id(1)
    t_get = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    _ = manager.filter_users(role='User')
    t_filter = (time.perf_counter() - t0) * 1000.0

    logger.info("[MARKER] display(ms)=%0.3f get(ms)=%0.3f filter(ms)=%0.3f", t_display, t_get, t_filter)
    print(manager.display_users(show_all=True, verbose=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
