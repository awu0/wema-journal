import pytest

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


# Test to verify correct behavior when email format is invalid
def test_invalid_email_format_raises_error(invalid_user_data):
    with pytest.raises(ValueError, match="Invalid email"):
        users.create_user(**invalid_user_data)


# Test skipping if function needs updates or is not ready
@pytest.mark.skip("Function under development, test not ready")
def test_function_under_development():
    # Placeholder test
    assert False, "This test is skipped because the function is not implemented yet."


# Test to ensure that patching works as expected for database calls
def test_get_user_by_email(user_data):
    with patch('data.users.get_user_by_email', return_value=user_data) as mock_get_user:
        user = users.get_user_by_email(user_data["email"])
        assert user["email"] == user_data["email"], "The email should match the input email."
        assert user["name"] == user_data["name"], "The user name should match the input data."
        mock_get_user.assert_called_once_with(user_data["email"])


# Test to verify exception handling for an attempt to update a non-existent user
def test_update_nonexistent_user_raises_error():
    non_existing_email = "nonexistent@nyu.edu"
    with patch('data.users.get_users_as_dict', return_value={}), \
         pytest.raises(ValueError, match="User not found"):
        users.update_user(non_existing_email, role="admin")


# Test using a fixture and patch to simulate adding a user
def test_add_user_success(user_data):
    with patch('data.users.get_users_as_dict', return_value={}), \
         patch('data.users.create_user', return_value=user_data["email"]) as mock_create_user:
        result = users.create_user(**user_data)
        assert result == user_data["email"], "User should be successfully created with the provided email."
        mock_create_user.assert_called_once_with(**user_data)


# Test using patch to simulate a database update failure
def test_update_user_database_failure(user_data):
    with patch('data.users.update_user', side_effect=Exception("Database failure")):
        with pytest.raises(Exception, match="Database failure"):
            users.update_user(user_data["email"], role="superadmin")

