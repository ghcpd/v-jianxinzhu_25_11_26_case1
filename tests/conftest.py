import logging
import pytest

from user_display_optimized import generate_sample_users, build_user_index, LOGGER_NAME


@pytest.fixture(autouse=True)
def _configure_logger():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    yield


@pytest.fixture()
def sample_users():
    return [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "role": "Admin",
            "status": "Active",
            "join_date": "2023-01-01",
            "last_login": "2025-11-01",
        },
        {
            "id": 2,
            "name": "Bob",
            "email": "bob@example.com",
            "role": "User",
            "status": "Inactive",
            "join_date": "2023-02-01",
            "last_login": "2025-11-02",
        },
    ]


@pytest.fixture()
def users_100():
    return generate_sample_users(100)


@pytest.fixture()
def users_1000():
    return generate_sample_users(1000)


@pytest.fixture()
def user_index_1000(users_1000):
    return build_user_index(users_1000)
