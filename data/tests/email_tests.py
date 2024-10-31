import pytest
from data.roles import TEST_CODE
import data.people as ppl

NO_AT = 'jkajsd'
NO_NAME = '@kalsj'
NO_DOMAIN = 'kajshd@'
NO_SUB_DOMAIN = 'kajshd@com'
DOMAIN_TOO_SHORT = 'kajshd@nyu.e'
DOMAIN_TOO_LONG = 'kajshd@nyu.eedduu'
ENDING_DOT = 'username@example.com.'
STARTS_WITH_PERIOD = '.user@example.com'
TEMP_EMAIL = 'temp_person@temp.org'

def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)


def test_is_valid_no_name():
    assert not ppl.is_valid_email(NO_NAME)


def test_is_valid_no_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)


def test_is_valid_no_sub_domain():
    assert not ppl.is_valid_email(NO_SUB_DOMAIN)


def test_is_valid_email_domain_too_short():
    assert not ppl.is_valid_email(DOMAIN_TOO_SHORT)


def test_is_valid_email_domain_too_long():
    assert not ppl.is_valid_email(DOMAIN_TOO_LONG)

def test_is_valid_email_domain_too_long():
    assert not ppl.is_valid_email(ENDING_DOT)

def test_is_valid_email_domain_too_long():
    assert not ppl.is_valid_email(STARTS_WITH_PERIOD)


@pytest.fixture(scope='function')
def temp_person():
    ret = ppl.create('Joe Smith', 'NYU', TEMP_EMAIL, TEST_CODE)
    yield ret
    ppl.delete(ret)
