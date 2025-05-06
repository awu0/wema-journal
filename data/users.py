"""
This module interfaces to our user data.
"""

import re
from typing import Optional

import bcrypt

import data.db_connect as dbc
import data.roles as rls
from data.roles import is_valid_role, get_roles
from examples.form_filler import PASSWORD

LEVEL = "level"
MIN_USER_NAME_LEN = 2

USER_COLLECT = 'user'
EMAIL = 'email'
NAME = 'name'
AFFILIATION = 'affiliation'
ROLE = 'role'
ROLES = 'roles'
PASSWORD = 'password'

client = dbc.connect_db()
print(f'{client=}')


class User:
    """
    Email is used as the unique identifier
    """

    def __init__(self, name: str, email: str, affiliation: str, roles: list = None):
        self.name = name
        self.email = email
        if roles:
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
            NAME: self.name,
            EMAIL: self.email,
            ROLES: self.roles,
            AFFILIATION: self.affiliation,
        }


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
            roles=user.get(ROLES, [])
        ) for user in db_users
    ]


def get_users_as_dict() -> dict:
    """
    Retrieve all users from the database and return them as a dictionary
    keyed by user email for JSON parsing.
    """
    try:
        db_users = dbc.read(USER_COLLECT)  # Fetch all user docs from the db.
        return {
            user[EMAIL]: {
                NAME: user.get(NAME, ""),
                EMAIL: user.get(EMAIL),
                ROLES: user.get(ROLES, []),
                AFFILIATION: user.get(AFFILIATION, ""),
            }
            for user in db_users
        }
    except Exception as e:
        print(f"Error retrieving users as dict: {e}")
        return {}


def create_user(name: str, email: str, password: str, affiliation: str, role: str = None) -> dict:
    users = get_users()
    
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    if role:
        new_user = User(name=name, email=email, affiliation=affiliation, roles=[role])
    else:
        new_user = User(name=name, email=email, affiliation=affiliation, roles=[])

    if check_valid_user(new_user):
        users.append(new_user)
        
        # save user to database
        new_user = new_user.to_dict()
        new_user[PASSWORD] = hashed_password
        
        dbc.create(USER_COLLECT, new_user)

    return get_users_as_dict()


def get_user(email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.
    """
    users = get_users()
    return next((user for user in users if user.email == email), None)


def update_user(email: str, name: str = None, role: str = None, affiliation: str = None) -> dict:
    user_to_update = get_user(email)

    if not user_to_update:
        raise ValueError(f"User with email {email} not found.")
    if not any([name, role, affiliation]):
        raise ValueError("No updates provided. Please specify at least one field to update.")

    updates = {}
    if name:
        user_to_update.name = name
        updates[NAME] = name

    if role:
        valid_roles = get_roles()
        if role not in valid_roles.values():
            raise ValueError(f"Invalid role '{role}'.")
        if role not in user_to_update.roles:
            user_to_update.roles.append(role)
        updates[ROLES] = user_to_update.roles

    if affiliation:
        user_to_update.affiliation = affiliation
        updates[AFFILIATION] = affiliation

    if not check_valid_user(user_to_update, True):
        raise ValueError("Updated user data is invalid.")

    # Update only the fields that changed
    dbc.update_doc(USER_COLLECT, {EMAIL: email}, updates)
    updated_user = get_user(email)
    return updated_user.to_dict()


def delete_user(email: str) -> Optional[User]:
    user = get_user(email)  # Get user before deleting
    if user:
        dbc.delete(USER_COLLECT, {EMAIL: email})
        return user
    return None


def check_valid_user(user: User, updating: bool = False) -> bool:
    users = get_users()

    if user in users and not updating:
        raise ValueError(f"Duplicate email: {user}")

    if user.roles and not is_valid_role(user.roles[0]):
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


def read() -> dict:
    people = dbc.read_dict(USER_COLLECT, EMAIL)
    print(f'{people=}')
    return people


def get_mh_fields(journal_code=None) -> list:
    return MH_FIELDS


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in get_mh_fields():
        mh_rec[field] = person.get(field, '')
    return mh_rec


def get_masthead() -> dict:
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_role = []
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_role.append(rec)
        masthead[text] = people_role
    return masthead


def has_role(person: dict, role: str) -> bool:
    if role in person.get(ROLES):
        return True
    return False


# For testing
def clear_users():
    """
    Clear all users from the database.
    Used primarily for testing purposes.
    """
    return dbc.delete_many(USER_COLLECT, {})  # delete all documents


def main():
    print(get_users())


if __name__ == "__main__":
    main()
