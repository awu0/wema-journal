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

