import pytest

from user_display_optimized import _build_sample_users


@pytest.fixture
def sample_users_small():
    return _build_sample_users(100)


@pytest.fixture
def sample_users_large():
    return _build_sample_users(1000)
