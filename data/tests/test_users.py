import users as usrs


def test_add_new_user(self):
    result = usrs.add_user("Johnson", 2)
    self.assertIn("Johnson", result)
    self.assertEqual(result["Johnson"]['level'], 2)


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
    users = usrs.update_users(user_name, new_level)

    assert user_name in users, "User should be found and updated."
    assert users[user_name]['level'] == new_level, "User level should be updated to 2."

    # Test case 2: Try to update a non-existing user
    non_existing_user = "NonExistentUser"
    users = usrs.update_users(non_existing_user, new_level)

    assert non_existing_user not in users, "Non-existing user should not be added to the dictionary."
