"""Comprehensive test suite for user_display_optimized module.

Tests cover:
- Empty list handling
- Missing keys handling
- Performance benchmarks (<50ms for 100 users, <100ms for 1000 users)
- Valid/invalid user ID lookups
- Single/multiple filter criteria
- Export formatting
- Logging marker capture
- Error handling without raising
"""

import pytest
import time
import logging
from user_display_optimized import (
    display_users,
    get_user_by_id,
    filter_users,
    export_users_to_string
)


class TestDisplayUsers:
    """Test suite for display_users function."""
    
    def test_display_users_with_sample_data(self, sample_users):
        """Test basic display functionality with sample data."""
        result = display_users(sample_users)
        
        assert "ID:1|Name:John Doe" in result
        assert "ID:2|Name:Jane Smith" in result
        assert "ID:3|Name:Bob Johnson" in result
        assert "[INFO] Processed 3 users." in result
    
    def test_display_users_empty_list(self):
        """Test display with empty user list."""
        result = display_users([])
        assert result == ""
    
    def test_display_users_without_summary(self, sample_users):
        """Test display without summary information."""
        result = display_users(sample_users, show_all=False)
        assert "[INFO] Processed" not in result
        assert "ID:1" in result
    
    def test_display_users_with_verbose(self, sample_users, caplog):
        """Test verbose mode logs processing messages."""
        with caplog.at_level(logging.INFO):
            display_users(sample_users, verbose=True)
        
        assert "[MARKER] Processing user 1" in caplog.text
        assert "[MARKER] Processing user 2" in caplog.text
    
    def test_display_users_with_missing_keys(self, users_with_missing_keys, caplog):
        """Test error handling for missing keys."""
        with caplog.at_level(logging.ERROR):
            result = display_users(users_with_missing_keys)
        
        # Should contain the complete user
        assert "ID:1|Name:Complete User" in result
        # Should log error for incomplete user
        assert "[MARKER] Missing key" in caplog.text
    
    def test_display_users_performance_100_users(self):
        """Test performance with 100 users (target: <50ms)."""
        users = [
            {
                'id': i,
                'name': f'User {i}',
                'email': f'user{i}@example.com',
                'role': 'User',
                'status': 'Active',
                'join_date': '2024-01-01',
                'last_login': '2025-11-26'
            }
            for i in range(100)
        ]
        
        start = time.perf_counter()
        result = display_users(users)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 50, f"Performance target missed: {elapsed:.2f}ms > 50ms"
        assert len(result) > 0
    
    def test_display_users_performance_1000_users(self, large_user_dataset):
        """Test performance with 1000 users (target: <100ms)."""
        start = time.perf_counter()
        result = display_users(large_user_dataset)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 100, f"Performance target missed: {elapsed:.2f}ms > 100ms"
        assert "[INFO] Processed 1000 users." in result
    
    def test_display_users_logging_markers(self, sample_users, caplog):
        """Test that logging uses [MARKER] format."""
        with caplog.at_level(logging.INFO):
            display_users(sample_users)
        
        assert "[MARKER] Starting display_users" in caplog.text
        assert "[MARKER] Completed display_users" in caplog.text


class TestGetUserById:
    """Test suite for get_user_by_id function."""
    
    def test_get_user_by_id_found(self, sample_users):
        """Test finding existing user by ID."""
        user = get_user_by_id(sample_users, 2)
        
        assert user is not None
        assert user['id'] == 2
        assert user['name'] == 'Jane Smith'
    
    def test_get_user_by_id_not_found(self, sample_users):
        """Test searching for non-existent user ID."""
        user = get_user_by_id(sample_users, 999)
        assert user is None
    
    def test_get_user_by_id_empty_list(self):
        """Test search in empty user list."""
        user = get_user_by_id([], 1)
        assert user is None
    
    def test_get_user_by_id_performance(self, large_user_dataset):
        """Test O(1) lookup performance (target: <1ms)."""
        start = time.perf_counter()
        user = get_user_by_id(large_user_dataset, 500)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 1, f"Performance target missed: {elapsed:.2f}ms > 1ms"
        assert user is not None
        assert user['id'] == 500
    
    def test_get_user_by_id_logging(self, sample_users, caplog):
        """Test logging for user lookup."""
        with caplog.at_level(logging.INFO):
            get_user_by_id(sample_users, 1)
        
        assert "[MARKER] Searching for user_id: 1" in caplog.text
        assert "[MARKER] Found user_id: 1" in caplog.text
    
    def test_get_user_by_id_not_found_logging(self, sample_users, caplog):
        """Test warning logging for missing user."""
        with caplog.at_level(logging.WARNING):
            get_user_by_id(sample_users, 999)
        
        assert "[MARKER] User not found: 999" in caplog.text
    
    def test_get_user_by_id_with_missing_id_key(self, caplog):
        """Test handling users with missing 'id' key."""
        users = [
            {'name': 'User without ID'},
            {'id': 2, 'name': 'User with ID'}
        ]
        
        with caplog.at_level(logging.INFO):
            user = get_user_by_id(users, 2)
        
        assert user is not None
        assert user['id'] == 2


class TestFilterUsers:
    """Test suite for filter_users function."""
    
    def test_filter_users_by_role(self, sample_users):
        """Test filtering users by role."""
        filtered = filter_users(sample_users, {'role': 'User'})
        
        assert len(filtered) == 1
        assert filtered[0]['name'] == 'Jane Smith'
    
    def test_filter_users_by_status(self, sample_users):
        """Test filtering users by status."""
        filtered = filter_users(sample_users, {'status': 'Active'})
        
        assert len(filtered) == 2
        assert all(u['status'] == 'Active' for u in filtered)
    
    def test_filter_users_by_name(self, sample_users):
        """Test filtering users by name (case-insensitive substring)."""
        filtered = filter_users(sample_users, {'name': 'john'})
        
        assert len(filtered) == 2  # John Doe and Bob Johnson
        names = [u['name'] for u in filtered]
        assert 'John Doe' in names
        assert 'Bob Johnson' in names
    
    def test_filter_users_multiple_criteria(self, sample_users):
        """Test filtering with multiple criteria."""
        filtered = filter_users(sample_users, {
            'status': 'Active',
            'role': 'Moderator'
        })
        
        assert len(filtered) == 1
        assert filtered[0]['name'] == 'Bob Johnson'
    
    def test_filter_users_no_criteria(self, sample_users):
        """Test that no criteria returns all users."""
        filtered = filter_users(sample_users, {})
        assert len(filtered) == len(sample_users)
    
    def test_filter_users_empty_list(self):
        """Test filtering empty user list."""
        filtered = filter_users([], {'role': 'Admin'})
        assert filtered == []
    
    def test_filter_users_no_matches(self, sample_users):
        """Test filtering with criteria that matches no users."""
        filtered = filter_users(sample_users, {'role': 'SuperAdmin'})
        assert len(filtered) == 0
    
    def test_filter_users_performance(self, large_user_dataset):
        """Test filtering performance with 100 users (target: <10ms)."""
        users_100 = large_user_dataset[:100]
        
        start = time.perf_counter()
        filtered = filter_users(users_100, {'status': 'Active'})
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 10, f"Performance target missed: {elapsed:.2f}ms > 10ms"
        assert len(filtered) > 0
    
    def test_filter_users_logging(self, sample_users, caplog):
        """Test logging for filter operations."""
        with caplog.at_level(logging.INFO):
            filter_users(sample_users, {'role': 'Admin'})
        
        assert "[MARKER] Filtering users with criteria:" in caplog.text
        assert "[MARKER] Filtered" in caplog.text
    
    def test_filter_users_with_missing_keys(self, caplog):
        """Test filtering gracefully handles missing keys."""
        users = [
            {'id': 1, 'name': 'User 1', 'role': 'Admin'},
            {'id': 2, 'name': 'User 2'},  # Missing 'role'
        ]
        
        filtered = filter_users(users, {'role': 'Admin'})
        assert len(filtered) == 1


class TestExportUsersToString:
    """Test suite for export_users_to_string function."""
    
    def test_export_users_basic_format(self, sample_users):
        """Test basic export formatting."""
        result = export_users_to_string(sample_users)
        
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result
        assert "User ID: 1" in result
        assert "Name: John Doe" in result
        assert "Email: john@example.com" in result
        assert "=" * 100 in result
        assert "-" * 100 in result
    
    def test_export_users_empty_list(self):
        """Test export with empty user list."""
        result = export_users_to_string([])
        
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result
    
    def test_export_users_contains_all_fields(self, sample_users):
        """Test that export includes all user fields."""
        result = export_users_to_string(sample_users[:1])
        
        assert "User ID: 1" in result
        assert "Name: John Doe" in result
        assert "Email: john@example.com" in result
        assert "Role: Admin" in result
        assert "Status: Active" in result
        assert "Join Date: 2023-01-15" in result
        assert "Last Login: 2025-11-26" in result
    
    def test_export_users_with_missing_keys(self, users_with_missing_keys, caplog):
        """Test export handles missing keys gracefully."""
        with caplog.at_level(logging.ERROR):
            result = export_users_to_string(users_with_missing_keys)
        
        # Should contain complete user
        assert "User ID: 1" in result
        # Should log error for incomplete user
        assert "[MARKER] Missing key" in caplog.text
    
    def test_export_users_logging(self, sample_users, caplog):
        """Test logging for export operations."""
        with caplog.at_level(logging.INFO):
            export_users_to_string(sample_users)
        
        assert "[MARKER] Starting export_users_to_string" in caplog.text
        assert "[MARKER] Completed export_users_to_string" in caplog.text


class TestIntegration:
    """Integration tests for combined operations."""
    
    def test_filter_and_display(self, sample_users):
        """Test filtering followed by display."""
        filtered = filter_users(sample_users, {'status': 'Active'})
        result = display_users(filtered)
        
        assert "ID:1|Name:John Doe" in result
        assert "ID:3|Name:Bob Johnson" in result
        assert "ID:2|Name:Jane Smith" not in result
    
    def test_lookup_and_export(self, sample_users):
        """Test user lookup followed by export."""
        user = get_user_by_id(sample_users, 2)
        result = export_users_to_string([user])
        
        assert "User ID: 2" in result
        assert "Name: Jane Smith" in result
    
    def test_complex_workflow(self, large_user_dataset):
        """Test complex workflow with filtering, lookup, and display."""
        # Filter admins
        admins = filter_users(large_user_dataset, {'role': 'Admin'})
        assert len(admins) > 0
        
        # Get specific user
        user = get_user_by_id(admins, admins[0]['id'])
        assert user is not None
        
        # Display filtered users
        result = display_users(admins[:10])
        assert len(result) > 0


class TestErrorHandling:
    """Test suite for error handling."""
    
    def test_display_users_handles_none_values(self, caplog):
        """Test handling None values in user data."""
        users = [
            {'id': 1, 'name': None, 'email': 'test@example.com',
             'role': 'User', 'status': 'Active', 'join_date': '2024-01-01',
             'last_login': '2025-11-26'}
        ]
        
        # Should not raise exception
        result = display_users(users)
        assert "ID:1" in result
    
    def test_filter_users_handles_exception(self, caplog):
        """Test that filter_users logs errors without raising."""
        with caplog.at_level(logging.ERROR):
            # Pass invalid data that might cause issues
            result = filter_users(None, {'role': 'Admin'})
        
        # Should return empty list on error
        assert result == []
    
    def test_display_users_general_exception(self, caplog):
        """Test handling of general exceptions in display_users."""
        users = [
            {'id': 1, 'name': 'Test User'},  # Missing required keys
        ]
        
        with caplog.at_level(logging.ERROR):
            result = display_users(users)
        
        # Should log error and continue
        assert "[MARKER] Missing key" in caplog.text or "[MARKER] Error processing user" in caplog.text
    
    def test_get_user_by_id_exception(self, caplog):
        """Test exception handling in get_user_by_id."""
        # Pass malformed data
        users = [{'name': 'No ID'}]
        
        with caplog.at_level(logging.ERROR):
            result = get_user_by_id(users, 1)
        
        # Should handle gracefully
        assert result is None
    
    def test_export_users_general_exception(self, caplog):
        """Test exception handling in export_users_to_string."""
        users = [
            {'id': 1},  # Missing most keys
        ]
        
        with caplog.at_level(logging.ERROR):
            result = export_users_to_string(users)
        
        # Should log error for incomplete data
        assert "[MARKER] Missing key" in caplog.text or "[MARKER] Error exporting user" in caplog.text


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=user_display_optimized", "--cov-report=term-missing"])
