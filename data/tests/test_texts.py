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
    mock_read_one.return_value = False
    mock_create.side_effect = Exception("Database insertion error")
    with pytest.raises(Exception) as excinfo:
        texts.create(test_data["key"], test_data["title"], test_data["text"])
    
    assert "Database insertion error" in str(excinfo.value)
    mock_read_one.assert_called_once_with(test_data["key"])
    mock_create.assert_called_once_with(texts.COLLECTION, test_data["entry"])

# Added Tests for Delete
@patch('data.db_connect.delete')
def test_delete_successful(mock_delete, mock_db, test_data):
    """Test deleting a text entry successfully."""
    mock_delete.return_value = 1
    result = texts.delete(test_data["key"])
    assert result is True
    mock_delete.assert_called_once_with(texts.COLLECTION, {texts.KEY: test_data["key"]})

@patch('data.db_connect.delete')
def test_delete_not_found(mock_delete, mock_db, test_data):
    """Test deleting a text entry that doesn't exist."""
    mock_delete.return_value = 0
    result = texts.delete(test_data["key"])
    assert result is False
    mock_delete.assert_called_once_with(texts.COLLECTION, {texts.KEY: test_data["key"]})

@patch('data.db_connect.delete')
def test_delete_empty_key(mock_delete, mock_db):
    """Test deleting a text entry with empty key."""
    mock_delete.return_value = 0
    result = texts.delete("")
    assert result is False
    mock_delete.assert_called_once_with(texts.COLLECTION, {texts.KEY: ""})

# Added Tests for Update
@patch('data.text.read_one')
@patch('data.db_connect.update_doc')
def test_update_title_only(mock_update_doc, mock_read_one, mock_db, test_data):
    """Test updating just the title of a text entry."""
    mock_read_one.side_effect = [
        test_data["entry"], 
        {**test_data["entry"], texts.TITLE: "Updated Title"}
    ]    
    result = texts.update(test_data["key"], title="Updated Title")
    assert result == {**test_data["entry"], texts.TITLE: "Updated Title"}
    assert mock_read_one.call_count == 2
    mock_update_doc.assert_called_once_with(
        texts.COLLECTION, 
        {texts.KEY: test_data["key"]}, 
        {texts.TITLE: "Updated Title"}
    )

@patch('data.text.read_one')
@patch('data.db_connect.update_doc')
def test_update_text_only(mock_update_doc, mock_read_one, mock_db, test_data):
    """Test updating just the text content of a text entry."""
    mock_read_one.side_effect = [
        test_data["entry"], 
        {**test_data["entry"], texts.TEXT: "Updated text content."}
    ]
    
    result = texts.update(test_data["key"], text="Updated text content.")
    assert result == {**test_data["entry"], texts.TEXT: "Updated text content."}
    assert mock_read_one.call_count == 2
    mock_update_doc.assert_called_once_with(
        texts.COLLECTION, 
        {texts.KEY: test_data["key"]}, 
        {texts.TEXT: "Updated text content."}
    )

@patch('data.text.read_one')
@patch('data.db_connect.update_doc')
def test_update_both_fields(mock_update_doc, mock_read_one, mock_db, test_data):
    """Test updating both title and text content of a text entry."""
    updated_entry = {
        texts.KEY: test_data["key"],
        texts.TITLE: "Updated Title",
        texts.TEXT: "Updated text content."
    }
    mock_read_one.side_effect = [test_data["entry"], updated_entry]
    result = texts.update(
        test_data["key"], 
        title="Updated Title", 
        text="Updated text content."
    )
    
    assert result == updated_entry
    assert mock_read_one.call_count == 2
    mock_update_doc.assert_called_once_with(
        texts.COLLECTION, 
        {texts.KEY: test_data["key"]}, 
        {texts.TITLE: "Updated Title", texts.TEXT: "Updated text content."}
    )
