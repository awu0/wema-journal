from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


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
    assert resp.status_code == OK
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
    user_email = "john@example.com"
    resp = TEST_CLIENT.delete(f"{ep.USERS_EP}/{user_email}")
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "Message" in resp_json
    assert resp_json["Message"] == "User deleted successfully!"



def test_adding_user():
    new_user_data = {
        "name": "John",
        "email": "john@example.com",
        "role": "editor",
        "affiliation": "NYU"
    }

    # PUT response to add user
    resp = TEST_CLIENT.put(
        f"{ep.USERS_EP}/{new_user_data['name']}/"
        f"{new_user_data['email']}/"
        f"{new_user_data['role']}/"
        f"{new_user_data['affiliation']}"
    )

    assert resp.status_code == 200

    resp_json = resp.get_json()

    assert "Message" in resp_json
    assert resp_json["Message"] == "User added successfully!"

    # assert all users are returned
    assert "Return" in resp_json
    all_users = resp_json["Return"]

    # make sure new user is in the response
    assert new_user_data["email"] in all_users
