import logging
import time

import pytest

from user_display_optimized import (
    build_user_index,
    display_users,
    export_users_to_string,
    filter_users,
    generate_sample_users,
    get_user_by_id,
    LOGGER_NAME,
)


logger = logging.getLogger(LOGGER_NAME)


def test_display_users_basic(sample_users):
    output = display_users(sample_users)
    lines = output.strip().split("\n")
    assert any("ID:1|Name:Alice" in line for line in lines)
    assert any("ID:2|Name:Bob" in line for line in lines)
    assert lines[-1] == "[INFO] Processed 2 users."


def test_display_users_missing_keys_logged(caplog):
    bad_users = [
        {
            "id": 3,
            "name": "Charlie",
            # missing email
            "role": "User",
            "status": "Active",
            "join_date": "2023-03-01",
            "last_login": "2025-11-03",
        }
    ]
    caplog.set_level(logging.ERROR, logger=LOGGER_NAME)
    output = display_users(bad_users)
    assert output.strip() == "[INFO] Processed 0 users."
    assert any("[DISPLAY][ERROR] Missing key 'email'" in rec.message for rec in caplog.records)


def test_get_user_by_id_with_index(users_1000, user_index_1000):
    user = get_user_by_id(users_1000, 500, user_index=user_index_1000)
    assert user is not None
    assert user["id"] == 500
    assert get_user_by_id(users_1000, 9999, user_index=user_index_1000) is None

    # performance: 10_000 lookups should be well under 10 ms
    start = time.perf_counter()
    for _ in range(10_000):
        get_user_by_id(users_1000, 500, user_index=user_index_1000)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < 10, f"Lookup took too long: {elapsed_ms:.2f} ms"


def test_get_user_by_id_mapping_branch(user_index_1000):
    # When users is already a mapping, the mapping branch is exercised
    user = get_user_by_id(user_index_1000, 10)
    assert user is not None and user["id"] == 10


def test_get_user_by_id_fallback_builds_index(sample_users):
    # Passing a list without user_index triggers fallback index build
    user = get_user_by_id(sample_users, 2)
    assert user is not None and user["id"] == 2


def test_filter_users(sample_users):
    active = filter_users(sample_users, {"status": "Active"})
    assert len(active) == 1 and active[0]["name"] == "Alice"

    admins = filter_users(sample_users, {"role": "Admin"})
    assert len(admins) == 1 and admins[0]["name"] == "Alice"

    by_name = filter_users(sample_users, {"name": "ali"})
    assert len(by_name) == 1 and by_name[0]["name"] == "Alice"


def test_filter_no_criteria_returns_all(sample_users):
    result = filter_users(sample_users, {})
    assert len(result) == len(sample_users)


def test_filter_users_missing_key_logs(caplog):
    users = [
        {
            "id": 1,
            # missing name
            "email": "x@example.com",
            "role": "User",
            "status": "Active",
            "join_date": "2023-01-01",
            "last_login": "2025-11-01",
        }
    ]
    caplog.set_level(logging.ERROR, logger=LOGGER_NAME)
    result = filter_users(users, {"name": "x"})
    assert result == []
    assert any("[FILTER][ERROR] Missing key" in rec.message for rec in caplog.records)


def test_export_users_to_string_format(sample_users):
    output = export_users_to_string(sample_users)
    lines = output.strip().split("\n")
    assert lines[0] == "USER_EXPORT_START"
    assert lines[-1] == "USER_EXPORT_END"
    assert any(line.startswith("User ID: 1") for line in lines)
    assert any(line.startswith("User ID: 2") for line in lines)


def test_export_users_skips_missing_fields(caplog):
    caplog.set_level(logging.ERROR, logger=LOGGER_NAME)
    bad_users = [{"id": 1, "name": "NoEmail"}]  # missing required fields
    output = export_users_to_string(bad_users)
    assert "NoEmail" not in output
    assert any("[DISPLAY][ERROR]" in rec.message for rec in caplog.records)


@pytest.mark.parametrize(
    "count, threshold_ms", [(100, 50), (1000, 100)]
)
def test_display_performance(count, threshold_ms):
    users = generate_sample_users(count)
    start = time.perf_counter()
    display_users(users, show_all=False)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < threshold_ms, f"display_users({count}) took {elapsed_ms:.2f} ms"


def test_empty_inputs():
    assert display_users([], show_all=True) == "[INFO] Processed 0 users.\n"
    assert filter_users([], {"role": "Admin"}) == []
    export_output = export_users_to_string([])
    assert export_output.startswith("USER_EXPORT_START")
    assert export_output.endswith("USER_EXPORT_END\n")


def test_logging_markers(caplog, sample_users):
    caplog.set_level(logging.DEBUG, logger=LOGGER_NAME)

    display_users(sample_users)
    filter_users(sample_users, {"role": "Admin"})
    build_user_index(sample_users)
    export_users_to_string(sample_users)

    messages = [rec.message for rec in caplog.records]
    assert any("[DISPLAY]" in m for m in messages)
    assert any("[FILTER]" in m for m in messages)
    assert any("[GET]" in m for m in messages)
    assert any("[EXPORT]" in m for m in messages)


def test_display_users_verbose_logs_debug(caplog, sample_users):
    caplog.set_level(logging.DEBUG, logger=LOGGER_NAME)
    display_users(sample_users, verbose=True)
    assert any("Processing user" in rec.message for rec in caplog.records)


def test_demo_runs(capsys):
    # Ensure the demo path executes without error and prints something
    import user_display_optimized as udo

    udo._demo()
    captured = capsys.readouterr()
    assert "ID:1" in captured.out or "User 1" in captured.out
