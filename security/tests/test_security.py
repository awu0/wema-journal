import pytest
import security.security as sec
from data.roles import Role

# Test user with editor role for testing
EDITOR_ROLE = [Role.EDITOR.value]
AUTHOR_ROLE = [Role.AUTHOR.value]
REFEREE_ROLE = [Role.REFEREE.value]
NON_EXISTENT_ROLE = ["non_existent_role"]
CONSULTING_EDITOR_ROLE = [Role.CONSULTING_EDITOR.value]
MANAGING_EDITOR_ROLE = [Role.MANAGING_EDITOR.value]

def test_check_login_good():
    assert sec.check_login(EDITOR_ROLE, login_key='any key will do for now')


def test_check_login_bad():
    assert not sec.check_login(EDITOR_ROLE)


def test_read():
    recs = sec.read()
    assert isinstance(recs, dict)
    for feature in recs:
        assert isinstance(feature, str)
        assert len(feature) > 0


def test_read_feature():
     feature = sec.read_feature(sec.PEOPLE)
     assert isinstance(feature, dict)


def test_is_permitted_no_such_feature():
    assert not sec.is_permitted('Non-existent feature', sec.CREATE, EDITOR_ROLE)


def test_is_permitted_action_missing():
    assert not sec.is_permitted(sec.PEOPLE, sec.PEOPLE_MISSING_ACTION, EDITOR_ROLE)


def test_is_permitted_bad_role():
    assert not sec.is_permitted(sec.TEXTS, sec.DELETE, NON_EXISTENT_ROLE)

def test_is_permitted_bad_check():
    """Test behavior with an invalid check function name"""
    sec.security_recs = None
    result = not sec.is_permitted(sec.BAD_FEATURE, sec.CREATE, EDITOR_ROLE)


def test_is_permitted_all_good():
    assert sec.is_permitted(sec.PEOPLE, sec.CREATE, EDITOR_ROLE,
                            login_key='any key for now')


def test_role_based_permissions():
    """Test that different roles have appropriate permissions"""
    # Editor should have delete permission
    assert sec.is_permitted(sec.PEOPLE, sec.DELETE, EDITOR_ROLE, 
                           login_key='any key for now')
    
    # Author should NOT have delete permission
    assert not sec.is_permitted(sec.PEOPLE, sec.DELETE, AUTHOR_ROLE,
                              login_key='any key for now')
    
    # Author should have update permission
    assert sec.is_permitted(sec.PEOPLE, sec.UPDATE, AUTHOR_ROLE,
                          login_key='any key for now')
    
    # All roles should have read permission
    for role in [role.value for role in Role]:
        assert sec.is_permitted(sec.PEOPLE, sec.READ, [role],
                              login_key='any key for now')


def test_multiple_roles():
    """Test that a user with multiple roles gets permissions from all roles"""
    # User with both author and editor roles
    multiple_roles = [Role.AUTHOR.value, Role.EDITOR.value]
    
    # Should have permissions from both roles
    assert sec.is_permitted(sec.PEOPLE, sec.UPDATE, multiple_roles,
                          login_key='any key for now')
    assert sec.is_permitted(sec.PEOPLE, sec.DELETE, multiple_roles,
                          login_key='any key for now')

def test_author_permissions():
    """Test that authors have the expected permissions"""
    # Authors should have create but not delete permissions for texts
    assert sec.is_permitted(sec.TEXTS, sec.CREATE, AUTHOR_ROLE, 
                           login_key='any key for now')
    assert not sec.is_permitted(sec.TEXTS, sec.DELETE, AUTHOR_ROLE,
                              login_key='any key for now')


def test_referee_permissions():
    """Test that referees have the expected permissions"""
    # Referees should not have create or delete permissions for texts
    assert not sec.is_permitted(sec.TEXTS, sec.CREATE, REFEREE_ROLE, 
                              login_key='any key for now')
    assert not sec.is_permitted(sec.TEXTS, sec.DELETE, REFEREE_ROLE,
                              login_key='any key for now')
    
def test_editor_permissions():
    """Test that editors have the expected permissions"""
    # Editors should have create and delete permissions for texts
    assert sec.is_permitted(sec.TEXTS, sec.CREATE, EDITOR_ROLE, 
                           login_key='any key for now')
    assert sec.is_permitted(sec.TEXTS, sec.DELETE, EDITOR_ROLE,
                           login_key='any key for now')
