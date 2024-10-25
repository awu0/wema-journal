"""
Manages the roles each user can have for our journal
"""

AUTHOR_CODE = "AU"
EDITOR_CODE = "ED"
REFREE_CODE = "RE"

roles = {
    AUTHOR_CODE: "Author",
    EDITOR_CODE: "Editor",
    REFREE_CODE: "Referee",
}

MH_ROLES = [AUTHOR_CODE, EDITOR_CODE, REFREE_CODE]

def get_roles() -> dict:
    return roles

def get_masthead_roles() -> dict:
    mh_roles = get_roles()
    del_mh_roles = []
    for role in mh_roles:
        if role not in MH_ROLES:
            del_mh_roles.append(role)
    for del_role in del_mh_roles:
        del mh_roles[del_role]
    return mh_roles

def get_role_codes() -> list:
    return list(roles.keys())


def is_valid_role(code: str) -> bool:
    return code in roles


def main():
    print(get_roles())
    print(get_masthead_roles())


if __name__ == "__main__":
    main()
