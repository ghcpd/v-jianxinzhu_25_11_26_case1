import time
import logging
from user_display_optimized import (
    display_users,
    get_user_by_id,
    filter_users,
    export_users_to_string,
    build_user_index,
)


def test_display_users_basic(sample_users):
    output = display_users(sample_users)
    assert "ID:1" in output
    assert "Processed 3 users" in output


def test_display_users_empty():
    output = display_users([])
    assert output.strip() == "[INFO] Processed 0 users." or output.strip() == ""


def test_display_users_missing_keys(caplog):
    caplog.set_level(logging.WARNING)
    bad_user = {"id": 99, "name": "Missing Keys"}
    output = display_users([bad_user])
    assert "<missing>" in output
    assert "Missing key" in caplog.text


def test_get_user_by_id_found_and_not_found(sample_users):
    idx = build_user_index(sample_users)
    user = get_user_by_id(sample_users, 2, index=idx)
    assert user and user["name"] == "Jane Smith"
    not_found = get_user_by_id(sample_users, 999, index=idx)
    assert not_found is None


def test_filter_users_single_and_multiple(sample_users):
    filtered = filter_users(sample_users, {"role": "Admin"})
    assert len(filtered) == 1 and filtered[0]["name"] == "John Doe"

    filtered = filter_users(sample_users, {"status": "Active", "name": "Bob"})
    assert len(filtered) == 1 and filtered[0]["id"] == 3


def test_export_users_to_string(sample_users):
    out = export_users_to_string(sample_users)
    assert "USER_EXPORT_START" in out
    assert "User ID: 1" in out


def test_logging_markers_captured(caplog, sample_users):
    caplog.set_level(logging.INFO)
    display_users(sample_users)
    assert "[USER-DISPLAY]" in caplog.text


def test_performance_display_100(users_100):
    start = time.perf_counter()
    display_users(users_100)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < 50, f"Expected <50ms, got {elapsed_ms:.2f}ms"


def test_performance_display_1000(users_1000):
    start = time.perf_counter()
    display_users(users_1000)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < 100, f"Expected <100ms, got {elapsed_ms:.2f}ms"


def test_build_user_index_skips_missing_id(caplog):
    caplog.set_level(logging.WARNING)
    bad = [{"name": "NoId"}, {"id": 5, "name": "HasId"}]
    from user_display_optimized import build_user_index
    idx = build_user_index(bad)
    assert 5 in idx and idx[5]["name"] == "HasId"
    assert "Skipping user without id" in caplog.text


def test_module_main_runs(caplog):
    caplog.set_level(logging.INFO)
    import runpy
    # Execute module as __main__ to exercise demo guard
    runpy.run_module("user_display_optimized", run_name="__main__")
    assert "[USER-DISPLAY]" in caplog.text
