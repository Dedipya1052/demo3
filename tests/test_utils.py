"""
Unit tests for utility functions.
"""

import pytest
import json
import tempfile
import os
from datetime import datetime
from src.utils import (
    setup_logging,
    load_json_file,
    save_json_file,
    format_timestamp,
    validate_email,
    safe_get
)


class TestLogging:
    """Test logging setup."""
    
    def test_setup_logging_default(self):
        """Test logging setup with default parameters."""
        logger = setup_logging()
        
        assert logger is not None
        assert logger.level == 20  # INFO level
        assert len(logger.handlers) >= 1
    
    def test_setup_logging_with_file(self):
        """Test logging setup with file handler."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            log_file = f.name
        
        try:
            logger = setup_logging(log_file=log_file)
            
            assert logger is not None
            assert len(logger.handlers) >= 2  # Console + file handler
            
            # Test logging to file
            logger.info("Test message")
            
            # Check if file was created and contains the message
            with open(log_file, 'r') as f:
                content = f.read()
                assert "Test message" in content
        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)


class TestJSONFileOperations:
    """Test JSON file operations."""
    
    def test_save_and_load_json_file(self):
        """Test saving and loading JSON files."""
        test_data = {
            "name": "Test User",
            "age": 30,
            "active": True,
            "tags": ["python", "testing"]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            file_path = f.name
        
        try:
            # Save data
            save_json_file(test_data, file_path)
            
            # Verify file exists
            assert os.path.exists(file_path)
            
            # Load data
            loaded_data = load_json_file(file_path)
            
            # Verify data matches
            assert loaded_data == test_data
            assert loaded_data["name"] == "Test User"
            assert loaded_data["age"] == 30
            assert loaded_data["active"] is True
            assert loaded_data["tags"] == ["python", "testing"]
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)
    
    def test_load_json_file_not_found(self):
        """Test loading non-existent JSON file."""
        with pytest.raises(FileNotFoundError):
            load_json_file("non_existent_file.json")
    
    def test_save_json_file_creates_directory(self):
        """Test that save_json_file creates parent directories."""
        test_data = {"test": "data"}
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "subdir", "test.json")
            
            # Save file (should create subdir)
            save_json_file(test_data, file_path)
            
            # Verify directory and file were created
            assert os.path.exists(os.path.dirname(file_path))
            assert os.path.exists(file_path)
            
            # Verify data was saved correctly
            loaded_data = load_json_file(file_path)
            assert loaded_data == test_data


class TestTimestampFormatting:
    """Test timestamp formatting."""
    
    def test_format_timestamp_default(self):
        """Test timestamp formatting with default (current time)."""
        timestamp = format_timestamp()
        
        # Should be a string
        assert isinstance(timestamp, str)
        
        # Should match expected format (YYYY-MM-DD HH:MM:SS)
        assert len(timestamp) == 19
        assert timestamp.count('-') == 2
        assert timestamp.count(':') == 2
        assert timestamp.count(' ') == 1
    
    def test_format_timestamp_with_datetime(self):
        """Test timestamp formatting with specific datetime."""
        test_datetime = datetime(2023, 1, 15, 14, 30, 45)
        timestamp = format_timestamp(test_datetime)
        
        assert timestamp == "2023-01-15 14:30:45"
    
    def test_format_timestamp_with_none(self):
        """Test timestamp formatting with None (should use current time)."""
        timestamp = format_timestamp(None)
        
        assert isinstance(timestamp, str)
        assert len(timestamp) == 19


class TestEmailValidation:
    """Test email validation."""
    
    def test_valid_emails(self):
        """Test valid email addresses."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user123@example.co.uk",
            "user@subdomain.example.com",
            "user@example-domain.com",
            "user@example.com",
            "user_name@example.com",
            "user-name@example.com",
            "user.name@example-domain.co.uk"
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True, f"Email should be valid: {email}"
    
    def test_invalid_emails(self):
        """Test invalid email addresses."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user@.com",
            "user..name@example.com",
            "user@example..com",
            "user@-example.com",
            "user@example-.com",
            "user name@example.com",
            "user@example com",
            "user@example",
            "user.example.com",
            "",
            "   ",
            None
        ]
        
        for email in invalid_emails:
            if email is not None:
                assert validate_email(email) is False, f"Email should be invalid: {email}"
    
    def test_email_edge_cases(self):
        """Test email validation edge cases."""
        # Very long email (should still be valid)
        long_email = "a" * 50 + "@" + "b" * 50 + ".com"
        assert validate_email(long_email) is True
        
        # Email with multiple dots in domain
        multi_dot_email = "user@example.co.uk"
        assert validate_email(multi_dot_email) is True


class TestSafeGet:
    """Test safe_get function."""
    
    def test_safe_get_existing_key(self):
        """Test safe_get with existing key."""
        test_dict = {"name": "John", "age": 30, "active": True}
        
        assert safe_get(test_dict, "name") == "John"
        assert safe_get(test_dict, "age") == 30
        assert safe_get(test_dict, "active") is True
    
    def test_safe_get_missing_key(self):
        """Test safe_get with missing key."""
        test_dict = {"name": "John", "age": 30}
        
        assert safe_get(test_dict, "email") is None
        assert safe_get(test_dict, "phone") is None
    
    def test_safe_get_with_default(self):
        """Test safe_get with custom default value."""
        test_dict = {"name": "John", "age": 30}
        
        assert safe_get(test_dict, "email", "default@example.com") == "default@example.com"
        assert safe_get(test_dict, "phone", 0) == 0
        assert safe_get(test_dict, "active", False) is False
    
    def test_safe_get_empty_dict(self):
        """Test safe_get with empty dictionary."""
        test_dict = {}
        
        assert safe_get(test_dict, "any_key") is None
        assert safe_get(test_dict, "any_key", "default") == "default"
    
    def test_safe_get_nested_dict(self):
        """Test safe_get with nested dictionary."""
        test_dict = {
            "user": {
                "name": "John",
                "settings": {
                    "theme": "dark",
                    "notifications": True
                }
            }
        }
        
        # Test with nested keys (safe_get doesn't handle nested access)
        assert safe_get(test_dict, "user") == {"name": "John", "settings": {"theme": "dark", "notifications": True}}
        assert safe_get(test_dict, "user", {}) == {"name": "John", "settings": {"theme": "dark", "notifications": True}}