"""Pytest configuration and shared fixtures."""

import pytest
import logging


@pytest.fixture
def sample_users():
    """Sample user data for testing."""
    return [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'Admin',
            'status': 'Active',
            'join_date': '2023-01-15',
            'last_login': '2025-11-26'
        },
        {
            'id': 2,
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'role': 'User',
            'status': 'Inactive',
            'join_date': '2023-06-20',
            'last_login': '2025-11-20'
        },
        {
            'id': 3,
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'role': 'Moderator',
            'status': 'Active',
            'join_date': '2024-02-10',
            'last_login': '2025-11-25'
        },
    ]


@pytest.fixture
def large_user_dataset():
    """Generate large user dataset for performance testing."""
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': 'User' if i % 3 != 0 else 'Admin',
            'status': 'Active' if i % 2 == 0 else 'Inactive',
            'join_date': '2024-01-01',
            'last_login': '2025-11-26'
        }
        for i in range(1, 1001)
    ]


@pytest.fixture
def users_with_missing_keys():
    """User data with missing keys for error handling tests."""
    return [
        {
            'id': 1,
            'name': 'Complete User',
            'email': 'complete@example.com',
            'role': 'Admin',
            'status': 'Active',
            'join_date': '2023-01-15',
            'last_login': '2025-11-26'
        },
        {
            'id': 2,
            'name': 'Incomplete User',
            'email': 'incomplete@example.com',
            # Missing 'role', 'status', 'join_date', 'last_login'
        },
    ]


@pytest.fixture
def caplog_with_marker(caplog):
    """Configure logging capture to detect [MARKER] logs."""
    caplog.set_level(logging.INFO)
    return caplog
