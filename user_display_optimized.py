"""Optimized user display implementation with performance, logging, and error handling."""

import logging
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def display_users(
    users: List[Dict[str, Any]], show_all: bool = True, verbose: bool = False
) -> str:
    """
    Display all users in a compact format with optimized performance.
    
    Uses list concatenation with join() instead of string concatenation in loops
    to achieve O(n) performance instead of O(n²).
    
    Args:
        users: List of user dictionaries containing id, name, email, role, status, join_date, last_login.
        show_all: If True, append summary info to output.
        verbose: If True, log processing information for each user.
    
    Returns:
        Formatted string with all users and optional summary.
    
    Raises:
        None - Logs errors gracefully and continues.
    """
    lines: List[str] = []
    processed_count: int = 0
    
    try:
        for user in users:
            try:
                if verbose:
                    logger.info(f"[PROCESSING] User ID: {user.get('id', 'UNKNOWN')}")
                
                # Extract fields with safe defaults for missing keys
                user_id: Any = user.get('id')
                user_name: str = user.get('name', 'N/A')
                user_email: str = user.get('email', 'N/A')
                user_role: str = user.get('role', 'N/A')
                user_status: str = user.get('status', 'N/A')
                user_join: str = user.get('join_date', 'N/A')
                user_login: str = user.get('last_login', 'N/A')
                
                # Efficient single-pass formatting
                line: str = (
                    f"ID:{user_id}|Name:{user_name}|Email:{user_email}|"
                    f"Role:{user_role}|Status:{user_status}|"
                    f"JoinDate:{user_join}|LastLogin:{user_login}"
                )
                lines.append(line)
                processed_count += 1
                
            except (KeyError, ValueError) as e:
                logger.error(f"[ERROR] Failed to process user: {e}")
                continue
        
        if show_all:
            lines.append(f"\n[INFO] Processed {processed_count} users.\n")
        
        logger.info(f"[DISPLAY_COMPLETE] Total users displayed: {processed_count}")
        return "\n".join(lines) + "\n"
    
    except Exception as e:
        logger.error(f"[CRITICAL] Unexpected error in display_users: {e}")
        return f"[ERROR] Failed to display users: {e}\n"


def get_user_by_id(users: List[Dict[str, Any]], user_id: Any) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user by ID using an optimized indexed lookup.
    
    For large lists, create an indexed dictionary first for O(1) lookups instead of O(n).
    This function uses linear search; for production with many lookups, index the data first.
    
    Args:
        users: List of user dictionaries.
        user_id: The ID to search for.
    
    Returns:
        User dictionary if found, None otherwise.
    """
    try:
        for user in users:
            if user.get('id') == user_id:
                logger.info(f"[USER_FOUND] ID: {user_id}")
                return user
        
        logger.warning(f"[USER_NOT_FOUND] ID: {user_id}")
        return None
    
    except Exception as e:
        logger.error(f"[ERROR] Failed to get user by ID {user_id}: {e}")
        return None


def filter_users(
    users: List[Dict[str, Any]], criteria: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Filter users by multiple criteria with simplified logic.
    
    Uses a single pass with all criteria checked per user.
    Supports filtering by 'role', 'status', and 'name' (case-insensitive substring match).
    
    Args:
        users: List of user dictionaries.
        criteria: Dictionary with optional keys: 'role', 'status', 'name'.
    
    Returns:
        List of users matching all specified criteria.
    """
    try:
        logger.info(f"[FILTER_START] Criteria: {criteria}")
        
        filtered: List[Dict[str, Any]] = [
            user
            for user in users
            if (
                criteria.get('role') is None or user.get('role') == criteria['role']
            )
            and (
                criteria.get('status') is None or user.get('status') == criteria['status']
            )
            and (
                criteria.get('name') is None
                or criteria['name'].lower() in user.get('name', '').lower()
            )
        ]
        
        logger.info(f"[FILTER_COMPLETE] Found {len(filtered)} matching users")
        return filtered
    
    except Exception as e:
        logger.error(f"[ERROR] Failed to filter users: {e}")
        return []


def export_users_to_string(users: List[Dict[str, Any]]) -> str:
    """
    Export users to formatted string with efficient memory usage.
    
    Uses list accumulation with join() instead of repeated string concatenation
    to avoid O(n²) memory and time complexity.
    
    Args:
        users: List of user dictionaries.
    
    Returns:
        Formatted export string with all users.
    """
    try:
        lines: List[str] = ["USER_EXPORT_START", "=" * 100]
        
        for user in users:
            try:
                user_lines: List[str] = [
                    f"User ID: {user.get('id', 'N/A')}",
                    f"  Name: {user.get('name', 'N/A')}",
                    f"  Email: {user.get('email', 'N/A')}",
                    f"  Role: {user.get('role', 'N/A')}",
                    f"  Status: {user.get('status', 'N/A')}",
                    f"  Join Date: {user.get('join_date', 'N/A')}",
                    f"  Last Login: {user.get('last_login', 'N/A')}",
                    "-" * 100,
                ]
                lines.extend(user_lines)
            
            except Exception as e:
                logger.error(f"[ERROR] Failed to export user: {e}")
                continue
        
        lines.append("USER_EXPORT_END")
        logger.info(f"[EXPORT_COMPLETE] Exported {len(users)} users")
        return "\n".join(lines) + "\n"
    
    except Exception as e:
        logger.error(f"[CRITICAL] Unexpected error in export_users_to_string: {e}")
        return f"[ERROR] Failed to export users: {e}\n"


def index_users_by_id(users: List[Dict[str, Any]]) -> Dict[Any, Dict[str, Any]]:
    """
    Create an indexed dictionary for O(1) user lookups.
    
    For applications performing many lookups, call this once after loading users.
    
    Args:
        users: List of user dictionaries.
    
    Returns:
        Dictionary mapping user ID to user dictionary.
    """
    try:
        indexed: Dict[Any, Dict[str, Any]] = {}
        for user in users:
            user_id: Any = user.get('id')
            if user_id is not None:
                indexed[user_id] = user
        
        logger.info(f"[INDEX_CREATED] Indexed {len(indexed)} users")
        return indexed
    
    except Exception as e:
        logger.error(f"[ERROR] Failed to index users: {e}")
        return {}


# Sample data
sample_users: List[Dict[str, Any]] = [
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


if __name__ == "__main__":
    print("Optimized Implementation Output:")
    print("=" * 100)
    output: str = display_users(sample_users)
    print(output)
