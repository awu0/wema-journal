import users as usrs


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, list)
    assert len(users) > 0  # at least one user!
    for user in users:
        assert isinstance(user.name, str)
        assert isinstance(user.email, str)
        assert isinstance(user.affiliation, str)
        assert isinstance(user.roles, list)

        assert len(user.name) >= usrs.MIN_USER_NAME_LEN


def test_add_new_user():
    result = usrs.create_user(
        name="Johnson", email="johson@nyu.edu", role="Author", affliation="NYU"
    )
    assert "johson@nyu.edu" in result, "The new user 'johson@nyu.edu' should be added."


# def test_update_users():
#     # Test case 1: Update an existing user
#     user_name = "Callahan"
#     new_level = 2
#     users = usrs.update_users(user_name, new_level)

#     assert user_name in users, "User should be found and updated."
#     assert users[user_name]['level'] == new_level, "User level should be updated to 2."

#     # Test case 2: Try to update a non-existing user
#     non_existing_user = "NonExistentUser"
#     users = usrs.update_users(non_existing_user, new_level)

#     assert non_existing_user not in users, "Non-existing user should not be added to the dictionary."
