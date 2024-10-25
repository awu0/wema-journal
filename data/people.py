"""
This module interfaces to our user data.
"""

import re

import data.roles as rls


def read():
    people = people_dict
    return people


def delete(_id):
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def is_valid_person(name: str, affiliation: str, email: str, role: str) -> bool:
    if email in people_dict:
        raise ValueError(f"Adding duplicate {email=}")
    if not is_valid_email(email):
        raise ValueError(f"Invalid email: {email}")
    if not rls.is_valid(role):
        raise ValueError(f"Invalid role: {role}")
    return True


def create(name: str, affiliation: str, email: str, role: str):
    pass


def get_masthead() -> dict:
    pass


def update():
    pass


def main():
    print(get_masthead())


if __name__ == "__main__":
    main()
