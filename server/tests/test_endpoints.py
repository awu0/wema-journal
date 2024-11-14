from http import HTTPStatus
from unittest.mock import patch

import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


@pytest.fixture
def sample_user():
    return  {
        "name": "John",
        "email": "john@example.com",
        "role": "editor",
        "affiliation": "NYU"
    }


@pytest.fixture
def incomplete_user():
    # missing affiliation field
    return  {
        "name": "John",
        "email": "john@example.com",
        "role": "editor",
        # "affiliation": "NYU"
    }


@pytest.fixture
def invalid_user():
    # invalid email
    return  {
        "name": "John",
        "email": "johnnybademail",
        "role": "editor",
        "affiliation": "NYU"
    }
    

def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_EP)
    resp_json = resp.get_json()
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)
    assert len(resp_json[ep.TITLE_RESP]) > 0


@patch('data.users.get_users_as_dict', autospec=True,
       return_value={'id': {'name': 'Joe Schmoe'}})
def test_read(mock_read):
    resp = TEST_CLIENT.get(ep.USERS_EP)
    assert resp.status_code == HTTPStatus.OK
    resp_json = resp.get_json()
    for _id, user in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert 'name' in user
    

def test_journal_name():
    resp = TEST_CLIENT.get(ep.JOURNAL_NAME_EP)
    resp_json = resp.get_json()

    assert ep.JOURNAL_NAME_RESP in resp_json

    journal_name = resp_json[ep.JOURNAL_NAME_RESP]
    assert isinstance(journal_name, str)
    assert len(journal_name) > 0
    assert journal_name == ep.JOURNAL_NAME


def test_getting_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert resp_json == ep.USERS


def test_deleting_users():
    user_email = "wilma@nyu.edu"
    
    resp = TEST_CLIENT.delete(f"{ep.USERS_EP}/{user_email}")
    assert resp.status_code == 200
    
    resp_json = resp.get_json()
    assert "Deleted" in resp_json
    assert resp_json["Deleted"]["email"] == user_email


def test_adding_user(sample_user):
    resp = TEST_CLIENT.post(ep.USERS_EP, json=sample_user)

    assert resp.status_code == HTTPStatus.CREATED

    resp_json = resp.get_json()

    assert "message" in resp_json
    assert resp_json["message"] == "User added successfully!"

    assert "return" in resp_json
    all_users = resp_json["return"]
    assert sample_user["email"] in all_users
    

def test_adding_user_missing_field_is_bad_request(incomplete_user):
    resp = TEST_CLIENT.post(ep.USERS_EP, json=incomplete_user)
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    resp_json = resp.get_json()

    assert "message" in resp_json
    assert resp_json["message"] == "Missing required fields"


def test_adding_user_invalid_field_is_bad_request(invalid_user):
    resp = TEST_CLIENT.post(ep.USERS_EP, json=invalid_user)
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    resp_json = resp.get_json()

    assert "message" in resp_json
    assert "Invalid email" in resp_json["message"]
    

def test_getting_fake_user_fails():
    fake_email = "fakeuseremail@fakeemaildomain.com"
    
    resp = TEST_CLIENT.get(f"{ep.USERS_EP}/{fake_email}/")
    assert resp.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.skip(reason="Not yet implemented")
def test_getting_user():
    pass
