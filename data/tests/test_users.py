import pytest
from unittest.mock import patch
import data.users as users


def test_get_users():
    all_users = users.get_users()
    assert isinstance(all_users, list)
    assert len(all_users) > 0  # at least one user!
    for user in all_users:
        assert isinstance(user.name, str)
        assert isinstance(user.email, str)
        assert isinstance(user.affiliation, str)
        assert isinstance(user.roles, list)

        assert len(user.name) >= users.MIN_USER_NAME_LEN


def test_add_new_user():
    result = users.create_user(
        name="Johnson", email="johson@nyu.edu", role="Author", affiliation="NYU"
    )
    assert "johson@nyu.edu" in result, "The new user 'johson@nyu.edu' should be added."


def test_valid_email_adds_new_user():
    new_user_data = {
        "name": "Fake User 0124",
        "email": "fake_user_0124@nyu.edu",
        "role": "editor",
        "affiliation": "NYU"
    }

    users.create_user(**new_user_data)
    assert new_user_data["email"] in users.get_users_as_dict(), "The new user 'johson@nyu.edu' should be added."


def test_invalid_email_raises_error():
    new_user_data = {
        "name": "Fake User without a valid email",
        "email": "not_an_email",
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


@pytest.mark.skip("Needs to be updated with our current code")
def test_update_users():
    # Test case 1: Update an existing user
    user_name = "Callahan"
    new_level = 2
    users = usrs.update_users(user_name, new_level)

    assert user_name in users, "User should be found and updated."
    assert users[user_name]['level'] == new_level, "User level should be updated to 2."

    # Test case 2: Try to update a non-existing user
    non_existing_user = "NonExistentUser"
    users = usrs.update_users(non_existing_user, new_level)

    assert non_existing_user not in users, "Non-existing user should not be added to the dictionary."


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


# def test_get_user_by_email():
#     # Simulate get_user_by_email returning a specific user dictionary
#     with patch('data.users.get_user_by_email', return_value={'name': 'Alice', 'email': 'alice@nyu.edu'}) as mock_get_user:
#         result = users.get_user_by_email('alice@nyu.edu')
#         assert result['name'] == 'Alice'
#         assert result['email'] == 'alice@nyu.edu'
#         # Check if the mocked function was called with the correct arguments
#         mock_get_user.assert_called_once_with('alice@nyu.edu')
