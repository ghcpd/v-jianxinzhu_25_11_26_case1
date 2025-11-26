"""Comprehensive test suite for optimized user display functions."""

import pytest
import logging
import time
from typing import List, Dict, Any

# Import the optimized module
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from user_display_optimized import (
    display_users,
    get_user_by_id,
    filter_users,
    export_users_to_string,
    index_users_by_id,
)


class TestDisplayUsers:
    """Tests for display_users function."""
    
    def test_display_users_basic(self, sample_users, caplog):
        """Test basic user display functionality."""
        caplog.set_level(logging.INFO)
        output = display_users(sample_users, show_all=True, verbose=False)
        
        assert output is not None
        assert "John Doe" in output
        assert "jane@example.com" in output
        assert "[INFO] Processed 5 users" in output
        assert "[DISPLAY_COMPLETE]" in caplog.text
    
    def test_display_users_empty_list(self, empty_users, caplog):
        """Test display_users with empty list."""
        caplog.set_level(logging.INFO)
        output = display_users(empty_users, show_all=True)
        
        assert "[INFO] Processed 0 users" in output
        assert output is not None
    
    def test_display_users_missing_keys(self, users_with_missing_keys, caplog):
        """Test display_users gracefully handles missing keys."""
        caplog.set_level(logging.INFO)
        output = display_users(users_with_missing_keys, show_all=True)
        
        assert "N/A" in output
        assert "[DISPLAY_COMPLETE]" in caplog.text
        assert output is not None
    
    def test_display_users_verbose_mode(self, sample_users, caplog):
        """Test display_users verbose logging."""
        caplog.set_level(logging.INFO)
        output = display_users(sample_users, verbose=True)
        
        assert "[PROCESSING]" in caplog.text
        assert "User ID: 1" in caplog.text
    
    def test_display_users_show_all_false(self, sample_users):
        """Test display_users with show_all=False."""
        output = display_users(sample_users, show_all=False, verbose=False)
        
        assert "Processed" not in output
        assert "John Doe" in output
    
    def test_display_users_performance_100(self, large_users):
        """Test performance: display 100 users in <50ms."""
        start = time.time()
        output = display_users(large_users)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        assert elapsed < 50, f"Display 100 users took {elapsed:.2f}ms (target: <50ms)"
        assert "User 1" in output
    
    def test_display_users_performance_1000(self, very_large_users):
        """Test performance: display 1000 users in <100ms."""
        start = time.time()
        output = display_users(very_large_users)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        assert elapsed < 100, f"Display 1000 users took {elapsed:.2f}ms (target: <100ms)"
        assert "User 1" in output
    
    def test_display_users_output_format(self, sample_users):
        """Test output formatting is correct."""
        output = display_users(sample_users, show_all=False)
        
        lines = output.strip().split('\n')
        first_user_line = lines[0]
        
        assert "ID:" in first_user_line
        assert "Name:" in first_user_line
        assert "Email:" in first_user_line
        assert "Role:" in first_user_line
        assert "Status:" in first_user_line


class TestGetUserById:
    """Tests for get_user_by_id function."""
    
    def test_get_user_by_id_valid(self, sample_users):
        """Test retrieving a user by valid ID."""
        user = get_user_by_id(sample_users, 1)
        
        assert user is not None
        assert user['id'] == 1
        assert user['name'] == 'John Doe'
    
    def test_get_user_by_id_invalid(self, sample_users, caplog):
        """Test retrieving a user by invalid ID."""
        caplog.set_level(logging.INFO)
        user = get_user_by_id(sample_users, 999)
        
        assert user is None
        assert "[USER_NOT_FOUND]" in caplog.text
    
    def test_get_user_by_id_empty_list(self, empty_users):
        """Test get_user_by_id with empty list."""
        user = get_user_by_id(empty_users, 1)
        assert user is None
    
    def test_get_user_by_id_logging(self, sample_users, caplog):
        """Test get_user_by_id logs correctly."""
        caplog.set_level(logging.INFO)
        get_user_by_id(sample_users, 1)
        
        assert "[USER_FOUND]" in caplog.text
    
    def test_get_user_by_id_performance(self, large_users):
        """Test get_user_by_id performance on 100 users (<1ms)."""
        start = time.time()
        user = get_user_by_id(large_users, 50)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        assert elapsed < 1, f"Get user took {elapsed:.2f}ms (target: <1ms)"
        assert user['id'] == 50


class TestFilterUsers:
    """Tests for filter_users function."""
    
    def test_filter_users_by_role(self, sample_users):
        """Test filtering users by role."""
        filtered = filter_users(sample_users, {'role': 'User'})
        
        assert len(filtered) > 0
        for user in filtered:
            assert user['role'] == 'User'
    
    def test_filter_users_by_status(self, sample_users):
        """Test filtering users by status."""
        filtered = filter_users(sample_users, {'status': 'Active'})
        
        assert len(filtered) > 0
        for user in filtered:
            assert user['status'] == 'Active'
    
    def test_filter_users_by_name(self, sample_users):
        """Test filtering users by name (substring)."""
        filtered = filter_users(sample_users, {'name': 'John'})
        
        assert len(filtered) >= 1
        assert any('John' in user['name'] for user in filtered)
    
    def test_filter_users_multiple_criteria(self, sample_users):
        """Test filtering with multiple criteria."""
        filtered = filter_users(sample_users, {'role': 'User', 'status': 'Active'})
        
        for user in filtered:
            assert user['role'] == 'User'
            assert user['status'] == 'Active'
    
    def test_filter_users_empty_criteria(self, sample_users):
        """Test filtering with empty criteria returns all users."""
        filtered = filter_users(sample_users, {})
        
        assert len(filtered) == len(sample_users)
    
    def test_filter_users_no_matches(self, sample_users):
        """Test filtering with criteria that match no users."""
        filtered = filter_users(sample_users, {'role': 'NonExistent'})
        
        assert len(filtered) == 0
    
    def test_filter_users_case_insensitive_name(self, sample_users):
        """Test name filtering is case-insensitive."""
        filtered_lower = filter_users(sample_users, {'name': 'john'})
        filtered_upper = filter_users(sample_users, {'name': 'JOHN'})
        
        assert len(filtered_lower) == len(filtered_upper)
    
    def test_filter_users_empty_list(self, empty_users):
        """Test filtering empty list."""
        filtered = filter_users(empty_users, {'role': 'Admin'})
        
        assert len(filtered) == 0
    
    def test_filter_users_performance_100(self, large_users):
        """Test filtering performance on 100 users (<10ms)."""
        start = time.time()
        filtered = filter_users(large_users, {'status': 'Active'})
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        assert elapsed < 10, f"Filter 100 users took {elapsed:.2f}ms (target: <10ms)"
        assert len(filtered) > 0


class TestExportUsersToString:
    """Tests for export_users_to_string function."""
    
    def test_export_users_to_string_basic(self, sample_users):
        """Test basic export functionality."""
        output = export_users_to_string(sample_users)
        
        assert "USER_EXPORT_START" in output
        assert "USER_EXPORT_END" in output
        assert "John Doe" in output
        assert "jane@example.com" in output
    
    def test_export_users_to_string_format(self, sample_users):
        """Test export formatting."""
        output = export_users_to_string(sample_users)
        
        assert "User ID:" in output
        assert "Name:" in output
        assert "Email:" in output
        assert "Role:" in output
        assert "Status:" in output
        assert "Join Date:" in output
        assert "Last Login:" in output
    
    def test_export_users_to_string_empty_list(self, empty_users):
        """Test export with empty list."""
        output = export_users_to_string(empty_users)
        
        assert "USER_EXPORT_START" in output
        assert "USER_EXPORT_END" in output
    
    def test_export_users_to_string_missing_keys(self, users_with_missing_keys, caplog):
        """Test export gracefully handles missing keys."""
        caplog.set_level(logging.INFO)
        output = export_users_to_string(users_with_missing_keys)
        
        assert "N/A" in output
        assert "USER_EXPORT_START" in output
    
    def test_export_users_to_string_performance_100(self, large_users):
        """Test export performance on 100 users (<50ms)."""
        start = time.time()
        output = export_users_to_string(large_users)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        assert elapsed < 50, f"Export 100 users took {elapsed:.2f}ms (target: <50ms)"
        assert output is not None
    
    def test_export_users_to_string_performance_1000(self, very_large_users):
        """Test export performance on 1000 users (<100ms)."""
        start = time.time()
        output = export_users_to_string(very_large_users)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        assert elapsed < 100, f"Export 1000 users took {elapsed:.2f}ms (target: <100ms)"
        assert output is not None


class TestIndexUsersById:
    """Tests for index_users_by_id function."""
    
    def test_index_users_by_id_basic(self, sample_users):
        """Test creating user index."""
        indexed = index_users_by_id(sample_users)
        
        assert len(indexed) == len(sample_users)
        assert 1 in indexed
        assert indexed[1]['name'] == 'John Doe'
    
    def test_index_users_by_id_lookup_performance(self, large_users):
        """Test indexed lookup is O(1) fast."""
        indexed = index_users_by_id(large_users)
        
        start = time.time()
        user = indexed.get(50)
        elapsed = (time.time() - start) * 1000000  # Convert to microseconds
        
        assert user is not None
        assert elapsed < 1000, f"Indexed lookup took {elapsed:.2f}µs (should be <1000µs)"
    
    def test_index_users_by_id_empty_list(self, empty_users):
        """Test indexing empty list."""
        indexed = index_users_by_id(empty_users)
        
        assert len(indexed) == 0
    
    def test_index_users_by_id_missing_id(self):
        """Test indexing with missing ID keys."""
        users = [
            {'name': 'User 1'},  # Missing 'id'
            {'id': 2, 'name': 'User 2'},
        ]
        indexed = index_users_by_id(users)
        
        assert 2 in indexed
        assert len(indexed) == 1  # Only user with ID should be indexed


class TestIntegration:
    """Integration tests for multiple functions."""
    
    def test_display_and_get_user(self, sample_users):
        """Test displaying users and retrieving one."""
        display_output = display_users(sample_users)
        user = get_user_by_id(sample_users, 1)
        
        assert user is not None
        assert "John Doe" in display_output
    
    def test_filter_and_export(self, sample_users):
        """Test filtering and exporting results."""
        filtered = filter_users(sample_users, {'role': 'User'})
        exported = export_users_to_string(filtered)
        
        assert len(filtered) > 0
        assert "USER_EXPORT_START" in exported
        for user in filtered:
            assert user['name'] in exported
    
    def test_index_and_display(self, large_users):
        """Test indexing and using indexed data."""
        indexed = index_users_by_id(large_users)
        
        # Convert back to list for display
        user_list = list(indexed.values())
        output = display_users(user_list)
        
        assert len(user_list) == len(large_users)
        assert output is not None
    
    def test_end_to_end_workflow(self, sample_users, caplog):
        """Test complete workflow: display, filter, export, index."""
        caplog.set_level(logging.INFO)
        
        # Display all users
        display_output = display_users(sample_users)
        assert display_output is not None
        
        # Filter users
        active_users = filter_users(sample_users, {'status': 'Active'})
        assert len(active_users) > 0
        
        # Export filtered users
        export_output = export_users_to_string(active_users)
        assert "USER_EXPORT_START" in export_output
        
        # Index users
        indexed = index_users_by_id(active_users)
        assert len(indexed) > 0
        
        # Retrieve from index
        user = indexed.get(1)
        if user:
            assert user['id'] == 1


class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_display_users_handles_exception(self, caplog):
        """Test display_users handles exceptions gracefully."""
        caplog.set_level(logging.INFO)
        # Pass invalid input
        output = display_users("not a list")
        
        assert "[CRITICAL]" in caplog.text or "[ERROR]" in caplog.text
    
    def test_display_users_none_input(self, caplog):
        """Test display_users handles None gracefully."""
        caplog.set_level(logging.INFO)
        output = display_users(None)
        
        assert "[CRITICAL]" in caplog.text or "[ERROR]" in caplog.text
    
    def test_get_user_by_id_with_exception(self, caplog):
        """Test get_user_by_id handles exceptions gracefully."""
        caplog.set_level(logging.INFO)
        # Pass invalid input
        result = get_user_by_id("not a list", 1)
        
        assert result is None
        assert "[ERROR]" in caplog.text
    
    def test_filter_users_handles_exception(self, sample_users, caplog):
        """Test filter_users handles exceptions gracefully."""
        caplog.set_level(logging.INFO)
        # filter_users with None criteria behaves like empty criteria (returns all)
        filtered = filter_users(sample_users, None)
        
        # This should trigger the exception handler
        assert "[ERROR]" in caplog.text or len(filtered) == 0
    
    def test_export_users_handles_exception(self, caplog):
        """Test export_users_to_string handles exceptions gracefully."""
        caplog.set_level(logging.INFO)
        # Pass invalid input
        output = export_users_to_string("not a list")
        
        assert "[CRITICAL]" in caplog.text or "[ERROR]" in caplog.text
    
    def test_index_users_handles_exception(self, caplog):
        """Test index_users_by_id handles exceptions gracefully."""
        caplog.set_level(logging.INFO)
        # Pass invalid input
        result = index_users_by_id("not a list")
        
        assert "[ERROR]" in caplog.text
        assert result == {}
    
    def test_logging_markers_present(self, sample_users, caplog):
        """Test that all logging markers are present."""
        caplog.set_level(logging.INFO)
        
        display_users(sample_users)
        get_user_by_id(sample_users, 1)
        filter_users(sample_users, {'role': 'User'})
        export_users_to_string(sample_users)
        index_users_by_id(sample_users)
        
        log_text = caplog.text
        assert "[DISPLAY_COMPLETE]" in log_text
        assert "[USER_FOUND]" in log_text or "[USER_NOT_FOUND]" in log_text
        assert "[FILTER_COMPLETE]" in log_text
        assert "[EXPORT_COMPLETE]" in log_text
        assert "[INDEX_CREATED]" in log_text
    
    def test_verbose_logging_markers(self, sample_users, caplog):
        """Test verbose mode logging markers."""
        caplog.set_level(logging.INFO)
        display_users(sample_users, verbose=True)
        
        assert "[PROCESSING]" in caplog.text


class TestTypeHints:
    """Tests to verify type hints are properly defined."""
    
    def test_function_signatures(self):
        """Test that functions have proper type hints."""
        import inspect
        
        # Get function signatures
        display_sig = inspect.signature(display_users)
        get_by_id_sig = inspect.signature(get_user_by_id)
        filter_sig = inspect.signature(filter_users)
        export_sig = inspect.signature(export_users_to_string)
        
        # Verify annotations exist
        assert 'users' in display_sig.parameters
        assert display_sig.return_annotation != inspect.Signature.empty
        
        assert 'users' in get_by_id_sig.parameters
        assert get_by_id_sig.return_annotation != inspect.Signature.empty
