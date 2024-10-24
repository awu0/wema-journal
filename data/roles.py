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


def get_roles() -> dict:
    return roles


def is_valid_role(code: str) -> bool:
    return code in roles


def main():
    print(get_roles())


if __name__ == "__main__":
    main()
