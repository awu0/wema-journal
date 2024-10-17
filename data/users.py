"""
This module interfaces to our user data.
"""

LEVEL = 'level'
MIN_USER_NAME_LEN = 2

USERS = {
    "Callahan": {
        LEVEL: 0,
    },
    "Reddy": {
        LEVEL: 1,
    },
}


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    return USERS


def add_user(name, level):
    users = get_users()
    if name not in users:
        users[name] = {LEVEL: level}
    return users


def delete_users(id):
    users = get_users()
    if id in users:
        del users[id]
        return id
    else:
        return None


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    users = get_users()
    return users


def update_users(uname, new_level):
    """
    Update the user's level in the users dictionary.
    Args:
        user_name (str): The name of the user to update.
        new_level (int): The new level to assign to the user.
    Returns:
        dict: The entire updated users dictionary.
    """
    users = get_users()
    if uname in users:
        users[uname][LEVEL] = new_level
    return users


def main():
    print(read())


if __name__ == '__main__':
    main()
