import data.text as texts
import pytest 
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_db():
    """Fixture to mock the database connection."""
    mock_client = MagicMock()
    with patch('data.db_connect.connect_db', return_value=mock_client) as mock_connect:
        yield mock_connect

# Fixture for test data
@pytest.fixture
def test_data():
    """Fixture for test data."""
    return {
        "key": "test_key",
        "title": "Test Title",
        "text": "This is test text content.",
        "entry": {
            texts.KEY: "test_key",
            texts.TITLE: "Test Title",
            texts.TEXT: "This is test text content."
        }
    }

# Tests for read_texts function
@patch('data.db_connect.read')
def test_read_texts(mock_read, mock_db):
    """Test reading all text entries."""
    # Set up the mock return value
    expected_result = {
        "user@example.com": {
            "key1": {"title": "Title 1", "text": "Text 1"},
            "key2": {"title": "Title 2", "text": "Text 2"}
        }
    }
    mock_read.return_value = expected_result
    
    # Call the function under test
    result = texts.read_texts()
    
    # Verify the result
    assert result == expected_result
    mock_read.assert_called_once_with(texts.COLLECTION)

# Tests for read_one function
@patch('data.db_connect.fetch_one')
def test_read_one_existing(mock_fetch_one, mock_db, test_data):
    """Test reading a single text entry that exists."""
    # Set up the mock return value
    mock_db_entry = test_data["entry"].copy()
    mock_db_entry['_id'] = 'some_id'  # Add _id field to simulate MongoDB document
    mock_fetch_one.return_value = mock_db_entry
    
    # Call the function under test
    result = texts.read_one(test_data["key"])
    
    # Verify the result
    assert result == test_data["entry"]
    mock_fetch_one.assert_called_once_with(texts.COLLECTION, {texts.KEY: test_data["key"]})