import pytest

from typing import List, Dict


@pytest.fixture()
def sample_users() -> List[Dict]:
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


@pytest.fixture()
def users_100() -> List[Dict]:
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': 'User' if i % 3 else 'Admin',
            'status': 'Active' if i % 2 else 'Inactive',
            'join_date': '2024-01-01',
            'last_login': '2025-11-26'
        }
        for i in range(1, 101)
    ]


@pytest.fixture()
def users_1000() -> List[Dict]:
    return [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': 'User' if i % 3 else 'Admin',
            'status': 'Active' if i % 2 else 'Inactive',
            'join_date': '2024-01-01',
            'last_login': '2025-11-26'
        }
        for i in range(1, 1001)
    ]
