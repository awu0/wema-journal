"""
This module interfaces to our user data.
"""

# import re
import data.roles as rls

LEVEL = "level"
MIN_USER_NAME_LEN = 2


class User:
    """
    Email is used as the unique identifier
    """

    def __init__(self, name: str, email: str, roles: list, affiliation: str):
        self.name = name
        self.email = email
        self.roles = roles
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


def get_users():
    return USERS


def get_users_as_dict():
    """
    Get users as dict for JSON parsing
    """
    return {user.email: user.to_dict() for user in USERS}


def create_user(name: str, email: str, role: str, affliation: str):
    users = get_users()
    new_user = User(name=name, email=email, affiliation=affliation, roles=[role])
    if check_valid_user(new_user):
        users.append(new_user)
    return get_users_as_dict()


def delete_user(email: str):
    users = get_users()
    for user in users:
        if user.email == email:
            users.remove(user)
            return user
    return None


def check_valid_user(user: User):
    users = get_users()
    if user in users:
        raise ValueError(f"Duplicate email: {user}")
    if not rls.is_valid_role(user.roles[0]):
        raise ValueError(f"Invalid role: {user}")
    return True


# def update_user(uname, new_level):
#     """
#     Update the user's level in the users dictionary.
#     Args:
#         user_name (str): The name of the user to update.
#         new_level (int): The new level to assign to the user.
#     Returns:
#         dict: The entire updated users dictionary.
#     """
#     users = get_users()
#     if uname in users:
#         users[uname][LEVEL] = new_level
#     return users


def main():
    print(get_users())


if __name__ == "__main__":
    main()
