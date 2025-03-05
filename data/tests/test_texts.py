import data.text as texts
import pytest 
from unittest.mock import patch, MagicMock
import copy 

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

# Testing Create
@patch('data.text.read_one')
@patch('data.db_connect.create')
def test_create_new_entry(mock_create, mock_read_one, mock_db, test_data):
    """Test creating a new text entry."""
    mock_read_one.return_value = False
    result = texts.create(test_data["key"], test_data["title"], test_data["text"])
    assert result == test_data["entry"]
    mock_read_one.assert_called_once_with(test_data["key"])
    mock_create.assert_called_once_with(texts.COLLECTION, test_data["entry"])

@patch('data.text.read_one')
def test_create_duplicate_key(mock_read_one, mock_db, test_data):
    """Test creating a text entry with a duplicate key."""
    mock_read_one.return_value = test_data["entry"]
    with pytest.raises(ValueError) as excinfo:
        texts.create(test_data["key"], test_data["title"], test_data["text"])
    assert f"Text with key '{test_data['key']}' already exists" in str(excinfo.value)
    mock_read_one.assert_called_once_with(test_data["key"])

@patch('data.text.read_one')
@patch('data.db_connect.create')
def test_create_with_empty_text(mock_create, mock_read_one, mock_db, test_data):
    """Test creating a text entry with empty text content."""
    mock_read_one.return_value = False
    expected_entry = copy.deepcopy(test_data["entry"])
    expected_entry[texts.TEXT] = ""
    
    result = texts.create(test_data["key"], test_data["title"], "")
    
    assert result == expected_entry
    mock_read_one.assert_called_once_with(test_data["key"])
    mock_create.assert_called_once_with(texts.COLLECTION, expected_entry)

@patch('data.text.read_one')
@patch('data.db_connect.create')
def test_create_db_error(mock_create, mock_read_one, mock_db, test_data):
    """Test creating a text entry when DB throws an error."""
    # Set up the mocks
    mock_read_one.return_value = False
    mock_create.side_effect = Exception("Database insertion error")
    
    # Call the function and check it throws the exception
    with pytest.raises(Exception) as excinfo:
        texts.create(test_data["key"], test_data["title"], test_data["text"])
    
    assert "Database insertion error" in str(excinfo.value)
    mock_read_one.assert_called_once_with(test_data["key"])
    mock_create.assert_called_once_with(texts.COLLECTION, test_data["entry"])
