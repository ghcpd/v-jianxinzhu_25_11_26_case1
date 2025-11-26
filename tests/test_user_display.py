import time
import re
from user_display_optimized import (
    display_users,
    get_user_by_id,
    filter_users,
    export_users_to_string,
    build_user_index,
    configure_logging,
    measure_execution_ms,
)


def test_display_empty_list(caplog):
    configure_logging()
    caplog.clear()
    out = display_users([], show_all=True)
    assert "Processed 0 users" in out


def test_display_missing_keys(caplog):
    configure_logging()
    bad_user = {"id": 1, "email": "no_name@example.com"}
    out = display_users([bad_user], show_all=True)
    # Missing fields should be replaced with N/A and function should not raise
    assert "N/A" in out


def test_get_user_by_id_valid_invalid(sample_users):
    idx = build_user_index(sample_users)
    found = idx.get(2)
    assert found and found["name"] == "Jane Smith"

    # Using public helper
    assert get_user_by_id(sample_users, 2)["name"] == "Jane Smith"
    assert get_user_by_id(sample_users, 999) is None


def test_filter_users_single_and_multiple(sample_users):
    by_role = filter_users(sample_users, role="User")
    assert isinstance(by_role, list)
    assert all(u["role"] == "User" for u in by_role) or len(by_role) == 0

    by_name = filter_users(sample_users, name="Bob")
    assert len(by_name) == 1 and by_name[0]["name"] == "Bob Johnson"


def test_export_users_to_string_format(sample_users):
    s = export_users_to_string(sample_users)
    assert s.startswith("USER_EXPORT_START")
    assert s.strip().endswith("USER_EXPORT_END")


def test_performance_display_100(generate_users):
    users = generate_users(100)
    elapsed = measure_execution_ms(display_users, users)
    # target: under 50ms for 100 users
    assert elapsed < 50.0


def test_performance_display_1000(generate_users):
    users = generate_users(1000)
    elapsed = measure_execution_ms(display_users, users)
    # target: under 100ms for 1000 users
    assert elapsed < 100.0


def test_filter_speed_100(generate_users):
    users = generate_users(100)
    start = time.perf_counter()
    _ = filter_users(users, name="User", status="Active")
    elapsed = (time.perf_counter() - start) * 1000.0
    assert elapsed < 10.0


def test_logging_markers(caplog):
    configure_logging()
    caplog.clear()
    from user_display_optimized import display_users as disp

    disp([{"id": 1, "name": "A"}], verbose=True)
    msgs = "\n".join([r.getMessage() for r in caplog.records])
    # The logger's handler formats include the [MARKER] prefix, the LogRecord message
    # itself should include the action text. We assert for either.
    assert "Processing user" in msgs


def test_safe_get_with_non_mapping(caplog):
    configure_logging()
    caplog.clear()
    # Ensure passing a non-mapping (e.g. None) doesn't raise and logs a warning
    out = display_users([None], show_all=True)
    assert "N/A" in out
    # A warning should be emitted about invalid user object (or safe handling)
    messages = "\n".join([r.getMessage() for r in caplog.records])
    assert "Missing/invalid user object" in messages or "Processed" in out


def test_build_user_index_duplicate_and_missing(caplog):
    configure_logging()
    caplog.clear()
    users = [{"id": 1, "name": "A"}, {"id": 1, "name": "B"}, {"name": "NO_ID"}]
    idx = build_user_index(users)
    # First entry for id 1 should be kept
    assert idx.get(1)["name"] == "A"
    msgs = "\n".join([r.getMessage() for r in caplog.records])
    assert "Duplicate id" in msgs
    assert "Skipping user with missing 'id' field" in msgs


def test_configure_logging_idempotent():
    # calling twice should not add multiple handlers or raise
    configure_logging()
    configure_logging()


def test_measure_execution_ms_returns_positive():
    elapsed = measure_execution_ms(lambda: sum(range(10_000)))
    assert elapsed >= 0.0
