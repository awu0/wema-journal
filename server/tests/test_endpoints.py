from http import HTTPStatus
from unittest.mock import patch

import pytest

import server.endpoints as ep
from data.users import User
from datetime import datetime, timedelta
import jwt

TEST_CLIENT = ep.app.test_client()
SECRET_KEY = 'test-secret-key'

import pytest
import jwt
from datetime import datetime, timedelta
from http import HTTPStatus

import server.endpoints as ep
from data.users import User

TEST_CLIENT = ep.app.test_client()
SECRET_KEY = 'test-secret-key'

# Set up a fixture to patch the SECRET_KEY in endpoints.py
@pytest.fixture(autouse=True)
def patch_secret_key(monkeypatch):
    """Ensure consistent SECRET_KEY between tests and application"""
    monkeypatch.setattr('server.endpoints.SECRET_KEY', SECRET_KEY)

# Create auth token as a fixture, not a function
@pytest.fixture
def auth_token():
    """Create a valid authentication token for testing."""
    admin_user = {
        "email": "admin@nyu.com",
        "password": "admin1234",
        "name": "Admin",
        "role": "editor",
        "affiliation": "NYU"
    }
    
    # Try to create the admin user
    create_resp = TEST_CLIENT.post(ep.USERS_EP, json=admin_user)
    #print(create_resp)
    
    # Try to login
    login_resp = TEST_CLIENT.post("/login", json={
        "email": admin_user["email"],
        "password": admin_user["password"]
    })
    
    if login_resp.status_code == 200:
        return login_resp.get_json()["token"]
    
    # If login fails, create manually
    payload = {
        'exp': datetime.now() + timedelta(days=1),
        'iat': datetime.now(),
        'sub': admin_user["email"]
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

@pytest.fixture
def auth_headers(auth_token):
    """Get headers with authentication token"""
    return {'Authorization': f'Bearer {auth_token}'}

@pytest.fixture
def sample_user(auth_headers):
    user = {
        "name": "John",
        "email": "john@example.com",
        "password": "password12",
        "role": "editor",
        "affiliation": "NYU"
    }
    
    TEST_CLIENT.delete(f"{ep.USERS_EP}/{user['email']}", headers=auth_headers)
    
    return user

@pytest.fixture
def sample_user_no_role(auth_headers):
    user = {
        "name": "Jack o' Lan",
        "email": "jackolan12@example.com",
        "password": "password12",
        "affiliation": "NYU"
    }

    TEST_CLIENT.delete(f"{ep.USERS_EP}/{user['email']}", headers=auth_headers)
    return user


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
        "password": "password12",
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


@patch('data.users.get_users', autospec=True, 
       return_value=[User(email='anotherperson@nyu.edu', name='Another Person', roles=[], affiliation='NYU')])
def test_get_user(mock_get_user):
    test_email = 'anotherperson@nyu.edu'
    resp = TEST_CLIENT.get(f"{ep.USERS_EP}?email={test_email}")
    assert resp.status_code == HTTPStatus.OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert test_email in resp_json
    user_data = resp_json[test_email]
    assert 'email' in user_data
    assert 'name' in user_data
    assert 'roles' in user_data
    assert 'affiliation' in user_data

    
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


@patch('data.users.delete_user', autospec=True)
def test_deleting_users(mock_delete, auth_headers):
    user_email = "wilma@nyu.edu"
    # Mock the return value of delete_user
    mock_user = User(
        email=user_email,
        name='Wilma',
        roles=['editor'],
        affiliation='NYU'
    )
    mock_delete.return_value = mock_user
    resp = TEST_CLIENT.delete(f"{ep.USERS_EP}/{user_email}", headers=auth_headers)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    assert "Deleted" in resp_json
    assert resp_json["Deleted"]["email"] == user_email
    # Verify mock was called with correct email
    mock_delete.assert_called_once_with(user_email)


def test_adding_user(auth_headers):
    # 1. First let's see what data we're sending
    test_data = {
        'name': 'John',
        'email': 'john_unique_test@example.com',  # Use a unique email to avoid duplicates
        'password': "abcd1234",
        'roles': ['editor'],
        'affiliation': 'NYU'  # Make sure all required fields are included
    }
    
    print(f"\nAttempting to add user with data: {test_data}")
    resp = TEST_CLIENT.post(f"{ep.USERS_EP}", json=test_data)
    
    # Print response for debugging
    print(f"Response status: {resp.status_code}")
    print(f"Response body: {resp.get_json() if resp.get_data() else 'No data'}")
    
    # Check if it's a duplicate email
    if resp.status_code == 400:
        resp_data = resp.get_json()
        if resp_data and 'message' in resp_data and 'Duplicate email' in resp_data['message']:
            # If it's a duplicate, try to delete first then retry
            print("Duplicate detected, trying to delete user first")
            resp = TEST_CLIENT.delete(f"{ep.USERS_EP}/{test_data['email']}", headers=auth_headers)
            
            # Try again
            resp = TEST_CLIENT.post(f"{ep.USERS_EP}", json=test_data)
            print(f"Second attempt response: {resp.status_code}")
            print(f"Second attempt body: {resp.get_json() if resp.get_data() else 'No data'}")
    
    # 5. Assert on the outcome
    assert resp.status_code == HTTPStatus.CREATED
    

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


def test_getting_user(sample_user):
    """Test getting a specific user returns correct data including roles"""
    # Create the user
    resp = TEST_CLIENT.post(ep.USERS_EP, json=sample_user)
    assert resp.status_code == HTTPStatus.CREATED
    
    # Get the user
    user_email = sample_user["email"]
    resp = TEST_CLIENT.get(f"{ep.USERS_EP}/{user_email}?role={sample_user['role']}")
    assert resp.status_code == HTTPStatus.OK

    resp_json = resp.get_json()
    assert "name" in resp_json
    assert resp_json["name"] == sample_user["name"]
    assert "email" in resp_json
    assert resp_json["email"] == sample_user["email"]
    assert "roles" in resp_json
    assert sample_user["role"] in resp_json["roles"]  # This should now pass
    assert "affiliation" in resp_json
    assert resp_json["affiliation"] == sample_user["affiliation"]


def test_get_user_not_found(sample_user):
    fake_email = "fakeuseremail@fakeemaildomain.com"

    resp = TEST_CLIENT.get(f"{ep.USERS_EP}/{fake_email}")
    assert resp.status_code == HTTPStatus.NOT_FOUND

    resp_json = resp.get_json()
    assert "message" in resp_json
    assert "not found" in resp_json["message"]


def test_update_user_success(sample_user):
    # Create the user
    resp = TEST_CLIENT.post(ep.USERS_EP, json=sample_user)
    assert resp.status_code == HTTPStatus.CREATED

    # Update the user
    updated_user_data = {
        "name": "John Doe",  # Changing name
        "role": "author",    # Changing role
    }

    user_email = sample_user["email"]
    resp = TEST_CLIENT.patch(f"{ep.USERS_EP}/{user_email}", json=updated_user_data)
    assert resp.status_code == HTTPStatus.OK

    resp_json = resp.get_json()
    assert "message" in resp_json
    assert resp_json["message"] == "User updated successfully"
    assert resp_json["updated_user"]["name"] == updated_user_data["name"]
    assert updated_user_data["role"] in resp_json["updated_user"]["roles"]


def test_update_user_invalid_role(sample_user):
    # Create the user
    resp = TEST_CLIENT.post(ep.USERS_EP, json=sample_user)
    assert resp.status_code == HTTPStatus.CREATED

    # Try to update with an invalid role
    invalid_role_data = {
        "role": "invalidrole42304"
    }

    user_email = sample_user["email"]
    resp = TEST_CLIENT.patch(f"{ep.USERS_EP}/{user_email}", json=invalid_role_data)
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    resp_json = resp.get_json()
    assert "message" in resp_json
    assert "Invalid role" in resp_json["message"]


def test_update_non_existing_user():
    fake_email = "fakeuseremail@fakeemaildomain.com"

    update_data = {
        "name": "Non Existent User",
    }

    resp = TEST_CLIENT.patch(f"{ep.USERS_EP}/{fake_email}", json=update_data)
    assert resp.status_code == HTTPStatus.NOT_FOUND

    resp_json = resp.get_json()
    assert "message" in resp_json
    assert "not found" in resp_json["message"]
