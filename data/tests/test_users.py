import users as usrs


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # at least one user!
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= usrs.MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.LEVEL in user
        assert isinstance(user[usrs.LEVEL], int)


def test_update_users():
    # Test case 1: Update an existing user
    user_name = "Callahan"
    new_level = 2
    updated_user = usrs.update_users(user_name, new_level)
    users = usrs.get_users()
    
    assert updated_user is not None, "User should be found and updated."
    assert updated_user['level'] == new_level, "User level should be updated to 2."
    assert users[user_name]['level'] == new_level, "Users dictionary should reflect the updated level."

    # Test case 2: Try to update a non-existing user
    non_existing_user = "NonExistentUser"
    result = usrs.update_users(non_existing_user, new_level)
    
    assert result is None, "Updating a non-existing user should return None."