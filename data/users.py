"""
This module interfaces to our user data.
"""

LEVEL = 'level'
MIN_USER_NAME_LEN = 2


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    users = {
        "Callahan": {
            LEVEL: 0,
        },
        "Reddy": {
            LEVEL: 1,
        },
    }
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


def main():
    print(read())


if __name__ == '__main__':
    main()
