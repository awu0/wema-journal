import roles


def test_get_roles():
    all_roles = roles.get_roles()

    assert isinstance(all_roles, dict)
    assert len(all_roles) > 0

    # assert all dictionary keys and items are strings
    for code, role in all_roles.items():
        assert isinstance(code, str)
        assert isinstance(role, str)
