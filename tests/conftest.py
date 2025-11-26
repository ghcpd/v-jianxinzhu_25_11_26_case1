"""Test configuration and fixtures for user display tests."""

import pytest
import logging
from typing import List, Dict, Any


@pytest.fixture
def sample_users() -> List[Dict[str, Any]]:
    """Provide sample user data for tests."""
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
        {
            'id': 4,
            'name': 'Alice Williams',
            'email': 'alice@example.com',
            'role': 'User',
            'status': 'Active',
            'join_date': '2024-05-12',
            'last_login': '2025-11-26'
        },
        {
            'id': 5,
            'name': 'Charlie Brown',
            'email': 'charlie@example.com',
            'role': 'User',
            'status': 'Active',
            'join_date': '2024-08-03',
            'last_login': '2025-11-24'
        },
    ]


@pytest.fixture
def empty_users() -> List[Dict[str, Any]]:
    """Provide empty user list for edge case testing."""
    return []


@pytest.fixture
def users_with_missing_keys() -> List[Dict[str, Any]]:
    """Provide user data with missing keys for error handling tests."""
    return [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            # Missing: role, status, join_date, last_login
        },
        {
            'id': 2,
            'name': 'Jane Smith',
            # Missing: email, role, status, join_date, last_login
        },
    ]


@pytest.fixture
def caplog_setup(caplog):
    """Setup caplog to capture logging output at INFO level."""
    caplog.set_level(logging.INFO)
    return caplog


@pytest.fixture
def large_users() -> List[Dict[str, Any]]:
    """Provide large dataset for performance testing (100+ users)."""
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': 'User' if i % 10 != 0 else 'Admin',
            'status': 'Active' if i % 5 != 0 else 'Inactive',
            'join_date': f'2023-{(i % 12) + 1:02d}-15',
            'last_login': f'2025-11-{(i % 26) + 1:02d}'
        }
        for i in range(1, 101)
    ]


@pytest.fixture
def very_large_users() -> List[Dict[str, Any]]:
    """Provide very large dataset for performance testing (1000+ users)."""
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': 'User' if i % 10 != 0 else 'Admin',
            'status': 'Active' if i % 5 != 0 else 'Inactive',
            'join_date': f'2023-{(i % 12) + 1:02d}-15',
            'last_login': f'2025-11-{(i % 26) + 1:02d}'
        }
        for i in range(1, 1001)
    ]
