"""
This module interfaces to our user data.
"""

import re
from typing import Optional

import data.db_connect as dbc
from data.roles import is_valid_role, get_roles

LEVEL = "level"
MIN_USER_NAME_LEN = 2

USER_COLLECT = 'user'
EMAIL = 'email'
NAME = 'name'
AFFILIATION = 'affiliation'
ROLE = 'role'


class User:
    """
    Email is used as the unique identifier
    """

    def __init__(self, name: str, email: str, affiliation: str, roles: list = None):
        self.name = name
        self.email = email
        if (roles):
            self.roles = roles
        else:
            self.roles = []
        self.affiliation = affiliation

    def __eq__(self, other):
        if isinstance(other, User):
            return self.email == other.email
        return False

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, roles={self.roles}, affiliation={self.affiliation})"

    def to_dict(self):
        """
        Convert the User object to a dictionary. For JSON operations
        """
        return {
            "name": self.name,
            "email": self.email,
            "roles": self.roles,
            "affiliation": self.affiliation,
        }


USERS = [
    User(name="William Ma", email="wilma@nyu.edu", roles=[], affiliation="NYU"),
    User(
        name="Another Person",
        email="anotherperson@nyu.edu",
        roles=[],
        affiliation="NYU",
    ),
]

client = dbc.connect_db()
print(f'{client=}')


def get_users() -> list[User]:
    """
    Retrieve all users from the database and return them as User objects.
    """
    db_users = dbc.read(USER_COLLECT)  # Fetch all user docs from the DB.
    return [
        User(
            name=user.get(NAME, ""),
            email=user[EMAIL],
            affiliation=user.get(AFFILIATION, ""),
            roles=user.get(ROLE, [])
        ) for user in db_users
    ]


def get_users_as_dict() -> dict:
    """
    Get users as dict for JSON parsing
    """
    return {user.email: user.to_dict() for user in USERS}
    """
    user = dbc.read_dict(USER_COLLECT, EMAIL)
    print(f'{user=}')
    return user
    """


def create_user(name: str, email: str, affiliation: str, role: str = None) -> dict:
    users = get_users()
    if (role):
        new_user = User(name=name, email=email, affiliation=affiliation, roles=[role])
    else:
        new_user = User(name=name, email=email, affiliation=affiliation, roles=[])

    if check_valid_user(new_user):
        users.append(new_user)
        # save user to database
        dbc.create(USER_COLLECT, new_user.to_dict())

    return get_users_as_dict()


def get_user(email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.
    """
    users = get_users()
    return next((user for user in users if user.email == email), None)


def delete_user(email: str) -> Optional[User]:
    users = get_users()
    print(f'{EMAIL=}, {email=}')
    for user in users:
        if user.email == email:
            users.remove(user)
            return user
    # return None
    return dbc.delete(USER_COLLECT, {EMAIL: email})


def check_valid_user(user: User, updating: bool = False) -> bool:
    users = get_users()

    if user in users and not updating:
        raise ValueError(f"Duplicate email: {user}")

    if not is_valid_role(user.roles[0]):
        raise ValueError(f"Invalid role: {user}")

    if not is_valid_email(user.email):
        raise ValueError(f"Invalid email: {user}")

    return True


def is_valid_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    return re.match(email_regex, email) is not None


name = "name"
affiliation = "affiliation"
MH_FIELDS = [name, affiliation]


def get_mh_fields(journal_code=None) -> list:
    return MH_FIELDS


def read() -> dict:
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    print('read() has been called')
    user_dict = get_users_as_dict()
    return user_dict
    user = dbc.read_dict(USER_COLLECT, EMAIL)
    print(f'{user=}')
    return user


def read_one(email: str) -> dict:
    roles = []
    # if role:
    #     roles.append(role)
    user = {NAME: name, AFFILIATION: affiliation,
            EMAIL: email, ROLE: roles}
    print(user)
    dbc.create(USER_COLLECT, user)
    return email


def update_user(email: str, name: str = None, role: str = None, affiliation: str = None) -> dict:
    user_to_update = get_user(email)

    if not user_to_update:
        raise ValueError(f"User with email {email} not found.")
    if not any([name, role, affiliation]):
        raise ValueError("No updates provided. Please specify at least one field to update.")

    if name:
        user_to_update.name = name

    if role:
        valid_roles = get_roles()
        if role not in valid_roles.values():
            raise ValueError(f"Invalid role '{role}'.")
        if role not in user_to_update.roles:
            user_to_update.roles.append(role)

    if affiliation:
        user_to_update.affiliation = affiliation

    if not check_valid_user(user_to_update, True):
        raise ValueError("Updated user data is invalid.")

    return user_to_update.to_dict()


def main():
    print(get_users())


if __name__ == "__main__":
    main()
