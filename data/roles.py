"""
Manages the roles each user can have for our journal
"""
from enum import Enum


class Role(Enum):
    AUTHOR = "author"
    REFEREE = "referee"
    EDITOR = "editor"
    CONSULTING_EDITOR = "consulting editor"
    MANAGING_EDITOR = "managing editor"


MH_ROLES = [Role.EDITOR, Role.CONSULTING_EDITOR, Role.MANAGING_EDITOR]


def read() -> dict:
    return {role.name: role.value for role in Role}


def get_roles() -> dict:
    return read()


def get_masthead_roles() -> dict:
    mh_roles = get_roles()
    del_mh_roles = []
    for role in mh_roles:
        if role not in MH_ROLES:
            del_mh_roles.append(role)
    for del_role in del_mh_roles:
        del mh_roles[del_role]
    return mh_roles


MH_FIELDS = ['name', 'affiliation']


def create_mh_rec(user: dict) -> dict:
    mh_rec = {}
    for field in MH_FIELDS:
        mh_rec[field] = user.get(field, '')
    return mh_rec


def is_valid_role(role: str) -> bool:
    return role.lower() in {role.value for role in Role}


def main():
    print(get_roles())
    print(get_masthead_roles())


if __name__ == "__main__":
    main()
