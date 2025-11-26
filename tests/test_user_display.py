import time
import re
import logging
from typing import Any

import pytest

from user_display_optimized import UserManager, _build_sample_users


def test_display_empty_list(caplog: Any):
    caplog.set_level(logging.INFO)
    manager = UserManager([])
    output = manager.display_users()
    assert "Processed 0 users" in output
    assert any("[MARKER]" in msg for msg in caplog.messages)


def test_get_user_by_id():
    users = _build_sample_users(10)
    manager = UserManager(users)
    u = manager.get_user_by_id(3)
    assert u is not None and u['id'] == 3
    assert manager.get_user_by_id(9999) is None


def test_filter_users():
    users = _build_sample_users(20)
    manager = UserManager(users)
    filtered = manager.filter_users(role='Admin')
    assert all(u['role'] == 'Admin' for u in filtered)
    filtered2 = manager.filter_users(name='User 1')
    assert any('User 1' in u['name'] for u in filtered2)


def test_export_users_to_string_format():
    users = _build_sample_users(3)
    manager = UserManager(users)
    s = manager.export_users_to_string()
    assert s.startswith('USER_EXPORT_START')
    assert 'USER_EXPORT_END' in s
    assert 'User ID: 1' in s


def test_missing_keys_handling(caplog: Any):
    caplog.set_level(logging.INFO)
    users = [{'id': 1, 'name': 'Incomplete'}]
    manager = UserManager(users)
    # Should not raise
    output = manager.display_users()
    assert 'N/A' in output
    # The index should contain the user, even if fields are missing
    assert manager.get_user_by_id(1) is not None


def test_logging_markers(caplog: Any):
    caplog.set_level(logging.INFO)
    users = _build_sample_users(5)
    manager = UserManager(users)
    _ = manager.filter_users(role='User')
    # Verify marker(s) logged
    assert any(re.search(r"\[MARKER\].*Filtering users", m) for m in caplog.messages)


def test_index_build_handles_malformed_user(caplog: Any):
    caplog.set_level(logging.INFO)

    class BadUser:
        def get(self, k):
            raise RuntimeError("broken")

    users = [{'id': 1, 'name': 'A'}, BadUser(), {'id': 2, 'name': 'B'}]
    # Should not raise during initialization
    manager = UserManager(users)
    assert manager.get_user_by_id(1) is not None
    assert manager.get_user_by_id(2) is not None
    assert any('Skipping malformed user' in m for m in caplog.messages)


def test_display_handles_exception_in_user_object(caplog: Any):
    caplog.set_level(logging.INFO)

    class BadUser:
        def get(self, k):
            raise RuntimeError("broken during display")

    users = [{'id': 1, 'name': 'A'}, BadUser(), {'id': 2, 'name': 'B'}]
    manager = UserManager(users)
    # Should not raise
    out = manager.display_users()
    assert 'Processed' in out
    # Ensure exception logged
    assert any('Error formatting user' in m for m in caplog.messages)


def test_duplicate_ids_index_last_wins():
    users = [{'id': 1, 'name': 'A'}, {'id': 1, 'name': 'B'}]
    manager = UserManager(users)
    # Last wins - name should be 'B'
    u = manager.get_user_by_id(1)
    assert u['name'] == 'B'


def test_export_users_counts():
    users = _build_sample_users(7)
    manager = UserManager(users)
    s = manager.export_users_to_string()
    assert s.count('User ID:') == 7


def test__build_sample_users_count():
    users = _build_sample_users(17)
    assert len(users) == 17


def test_display_verbose_logs(caplog: Any):
    caplog.set_level(logging.INFO)
    users = _build_sample_users(3)
    manager = UserManager(users)
    _ = manager.display_users(verbose=True)
    assert any('Processing user' in m for m in caplog.messages)


def test_main_runs_quickly():
    # call main to exercise top-level timing code; main already prints manager output
    from user_display_optimized import main
    assert main() == 0


def test_performance_small_and_large():
    # Small
    users_small = _build_sample_users(100)
    manager_small = UserManager(users_small)
    t0 = time.perf_counter()
    _ = manager_small.display_users(show_all=False)
    t_small_ms = (time.perf_counter() - t0) * 1000.0
    assert t_small_ms < 50, f"Display 100 users should be <50ms, actual {t_small_ms:.2f}ms"

    # Large
    users_large = _build_sample_users(1000)
    manager_large = UserManager(users_large)
    t0 = time.perf_counter()
    _ = manager_large.display_users(show_all=False)
    t_large_ms = (time.perf_counter() - t0) * 1000.0
    assert t_large_ms < 100, f"Display 1000 users should be <100ms, actual {t_large_ms:.2f}ms"

    # Filter performance
    t0 = time.perf_counter()
    _ = manager_large.filter_users(role='User')
    t_filter_ms = (time.perf_counter() - t0) * 1000.0
    assert t_filter_ms < 10, f"Filter 100 users should be <10ms, actual {t_filter_ms:.2f}ms"

    # Get user by ID should be very fast
    t0 = time.perf_counter()
    _ = manager_large.get_user_by_id(1)
    t_get_ms = (time.perf_counter() - t0) * 1000.0
    assert t_get_ms < 1, f"Get by id should be <1ms, actual {t_get_ms:.4f}ms"
