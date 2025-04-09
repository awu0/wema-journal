import pytest
import security.security as sec


def test_check_login_good():
    assert sec.check_login(sec.GOOD_USER_ID, login_key='any key will do for now')


def test_check_login_bad():
    assert not sec.check_login(sec.GOOD_USER_ID)


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
    assert sec.is_permitted('Non-existent feature', sec.CREATE, 'any user')


def test_is_permitted_action_missing():
    assert sec.is_permitted(sec.PEOPLE, sec.PEOPLE_MISSING_ACTION, 'any user')


def test_is_permitted_bad_user():
    assert not sec.is_permitted(sec.PEOPLE, sec.CREATE, 'non-existent user')


def test_is_permitted_bad_check():
    with pytest.raises(ValueError):
        sec.is_permitted(sec.BAD_FEATURE, sec.CREATE, sec.GOOD_USER_ID)


def test_is_permitted_all_good():
    assert sec.is_permitted(sec.PEOPLE, sec.CREATE, sec.GOOD_USER_ID,
                            login_key='any key for now')
    
def test_get_user_permissions():
    """
    Test that get_user_permissions correctly returns all permissions for a specific user.
    """
    # Reset security records to ensure a clean test state
    sec.security_recs = None
    
    # Get permissions for GOOD_USER_ID
    good_user_perms = sec.get_user_permissions(sec.GOOD_USER_ID)
    assert isinstance(good_user_perms, dict), "Should return a dictionary"
    assert len(good_user_perms) > 0, "GOOD_USER_ID should have permissions"
    assert sec.PEOPLE in good_user_perms, "GOOD_USER_ID should have access to PEOPLE feature"
    assert sec.CREATE in good_user_perms[sec.PEOPLE], "GOOD_USER_ID should have CREATE permission for PEOPLE"
    assert sec.BAD_FEATURE in good_user_perms, "GOOD_USER_ID should have access to BAD_FEATURE"
    assert sec.CREATE in good_user_perms[sec.BAD_FEATURE], "GOOD_USER_ID should have CREATE permission for BAD_FEATURE"
    
    # Check non-existent user has no permissions
    nonexistent_perms = sec.get_user_permissions("nonexistent@example.com")
    assert isinstance(nonexistent_perms, dict), "Should return a dictionary"
    assert len(nonexistent_perms) == 0, "Non-existent user should have no permissions"
    
    # Check non-existent feature is not in permissions
    assert "NonExistentFeature" not in good_user_perms, "Non-existent feature should not be in permissions"
