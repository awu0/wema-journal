import pytest

import data.users as users
from data.users import get_user


@pytest.fixture
def sample_user():
    return  {
        "name": "John",
        "email": "john@nyu.edu",
        "role": "editor",
        "affiliation": "NYU Alumni"
    }


def test_get_users():
    # Create a test user first
    users.create_user(
        name="Test User",
        email="test@nyu.edu",
        password="password12",
        role="editor",
        affiliation="NYU"
    )
    
    all_users = users.get_users()
    assert isinstance(all_users, list)
    assert len(all_users) > 0  # now this will pass
    for user in all_users:
        assert isinstance(user.name, str)
        assert isinstance(user.email, str)
        assert isinstance(user.affiliation, str)
        assert isinstance(user.roles, list)
        assert len(user.name) >= users.MIN_USER_NAME_LEN


def test_add_new_user():
    result = users.create_user(
        name="Bill", email="bill@nyu.edu", password="password12", role="Author", affiliation="NYU"
    )
    assert "bill@nyu.edu" in result, "The new user 'bill@nyu.edu' should be added."


def test_valid_email_adds_new_user():
    new_user_data = {
        "name": "Faker",
        "email": "faker@nyu.edu",
        "password": "password12",
        "role": "editor",
        "affiliation": "NYU"
    }

    users.create_user(**new_user_data)
    assert new_user_data["email"] in users.get_users_as_dict(), "The new user 'faker@nyu.edu' should be added."


def test_invalid_email_raises_error():
    new_user_data = {
        "name": "Fake User without a valid email",
        "email": "not_an_email",
        "password": "password12",
        "role": "author",
        "affiliation": "NYU"
    }

    with pytest.raises(ValueError, match="Invalid email"):
        users.create_user(**new_user_data)

    # new user isn't in returned users
    assert new_user_data["email"] not in users.get_users_as_dict(), "The new user 'johson@nyu.edu' should NOT be added."


def test_email_no_subdomain_is_invalid():
    temp_email = "testuser@com"
    assert not users.is_valid_email(temp_email)
    

def test_email_no_username_is_invalid():
    temp_email = "@nyu.edu"
    assert not users.is_valid_email(temp_email)


def test_get_mh_fields():
    flds = users.get_mh_fields()
    assert isinstance(flds, list)
    assert len(flds) > 0


def test_update_users():
    # First create a user to update
    email = "faker@nyu.edu"
    users.create_user(
        name="Faker",
        email=email,
        password="password12",
        role="editor",
        affiliation="NYU"
    )
    
    new_name = "Lee"
    new_roles = ["author"]
    new_affiliation = "NYU Alumni"
    
    returned_user = users.update_user(email=email, name=new_name, roles=new_roles, affiliation=new_affiliation)
    updated_user = get_user(email).to_dict()

    assert updated_user == returned_user, "Updated user in the database should equal returned user."
    assert updated_user["name"] == new_name, "User name should be updated."
    assert new_roles == updated_user["roles"], "New role should be added to user roles."
    assert updated_user["affiliation"] == new_affiliation, "User affiliation should be updated."

    # Test case 2: Try to update a non-existing user
    non_existing_email = "nonexistent@nyu.edu"
    with pytest.raises(ValueError, match=f"User with email {non_existing_email} not found."):
        users.update_user(email=non_existing_email, name="Nonexistent User")

    # Test case 3: Try to update with no fields provided
    with pytest.raises(ValueError, match="No updates provided. Please specify at least one field to update."):
        users.update_user(email=email)


@pytest.fixture
def valid_user_data():
    """Fixture providing valid user data."""
    return {
        "name": "Valid User",
        "email": "valid_user@nyu.edu",
        "role": "admin",
        "affiliation": "NYU"
    }


@pytest.fixture
def invalid_user_data():
    """Fixture providing invalid user data."""
    return {
        "name": "Invalid User",
        "email": "not_an_email",
        "role": "editor",
        "affiliation": "NYU"
    }


@pytest.fixture(autouse=True)
def clean_test_database():
    """Fixture to clean up the test database before each test"""
    yield
    users.clear_users()


# def test_get_user_by_email():
#     # Simulate get_user_by_email returning a specific user dictionary
#     with patch('data.users.get_user_by_email', return_value={'name': 'Alice', 'email': 'alice@nyu.edu'}) as mock_get_user:
#         result = users.get_user_by_email('alice@nyu.edu')
#         assert result['name'] == 'Alice'
#         assert result['email'] == 'alice@nyu.edu'
#         # Check if the mocked function was called with the correct arguments
#         mock_get_user.assert_called_once_with('alice@nyu.edu')
