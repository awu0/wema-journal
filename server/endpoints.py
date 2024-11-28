"""
This is the file containing all the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

import werkzeug.exceptions as wz
from flask import Flask, request  # , request
from flask_cors import CORS
from flask_restx import Resource, Api, fields  # Namespace, fields

import data.users as users
from data.users import get_user

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = "/endpoints"
ENDPOINT_RESP = "Available endpoints"
HELLO_EP = "/hello"
HELLO_RESP = "hello"
TITLE_EP = "/title"
TITLE_RESP = "Title"
TITLE = "The Journal of API Technology"
EDITOR_RESP = "Editor"
EDITOR = "ejc369@nyu.edu"
DATE_RESP = "Date"
DATE = "2024-09-24"
JOURNAL_NAME_EP = "/journal-name"
JOURNAL_NAME_RESP = "Journal Name"
JOURNAL_NAME = "wema"
USERS_EP = "/users"
USERS = users.get_users_as_dict()

USER_CREATE_FIELDS = api.model('AddNewUserEntry', {
    users.NAME: fields.String(required=True, description="User's name"),
    users.EMAIL: fields.String(required=True, description="User's email"),
    users.AFFILIATION: fields.String(required=True, description="User's affiliation"),
    users.ROLE: fields.String(required=True, description="User's role"),
})

USER_UPDATE_FIELDS = api.model('UpdateUserEntry', {
    users.NAME: fields.String(description="User's name"),
    users.EMAIL: fields.String(description="User's email"),
    users.AFFILIATION: fields.String(description="User's affiliation"),
    users.ROLE: fields.String(description="User's role"),
})


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """

    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        return {HELLO_RESP: "world"}


@api.route(ENDPOINT_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """

    def get(self):
        """
        The `get()` method will return a sorted list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(TITLE_EP)
class JournalTitle(Resource):
    """
    This class handles creating, reading, updating
    and deleting the journal title.
    """

    def get(self):
        """
        Retrieve the journal title.
        """
        return {
            TITLE_RESP: TITLE,
            EDITOR_RESP: EDITOR,
            DATE_RESP: DATE,
        }


@api.route(JOURNAL_NAME_EP)
class JournalName(Resource):
    """
    This is our group dev env assignment.
    """

    def get(self):
        """
        Shows our journal name which is wema.
        """
        return {
            JOURNAL_NAME_RESP: JOURNAL_NAME,
        }


@api.route(USERS_EP)
class Users(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """

    def get(self):
        """
        Retrieve the journal people.
        """
        return users.get_users_as_dict()

    @api.expect(USER_CREATE_FIELDS)
    @api.response(HTTPStatus.CREATED, "User created successfully")
    @api.response(HTTPStatus.BAD_REQUEST, "Invalid data provided")
    def post(self):
        """
        Adds a new user with given JSON data
        """
        data = request.json
        required_fields = ["name", "email", "role", "affiliation"]

        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, HTTPStatus.BAD_REQUEST

        try:
            users.create_user(
                name=data["name"],
                email=data["email"],
                role=data["role"],
                affiliation=data["affiliation"],
            )
            return {"message": "User added successfully!", "added_user": data}, HTTPStatus.CREATED
        except ValueError as e:
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST


@api.route(f"{USERS_EP}/<_email>")
class User(Resource):
    """
    This class handles creating, reading, updating, and deleting users
    """

    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "No such person")
    def get(self, _email):
        user = get_user(_email).to_dict()
        if user:
            return user
        else:
            raise wz.NotFound(f'No such user: {_email}')

    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "No such person")
    def delete(self, _email):
        ret = users.delete_user(_email)
        print(f"{ret=}")
        if ret is not None:
            return {"Deleted": ret.to_dict()}
        else:
            return wz.NotFound(f"No such person: {_email}")

    @api.expect(USER_UPDATE_FIELDS)
    @api.response(HTTPStatus.CREATED, "User updated successfully")
    @api.response(HTTPStatus.NOT_FOUND, "User not found")
    @api.response(HTTPStatus.BAD_REQUEST, "Invalid data provided")
    def patch(self, _email):
        """
        Updates a user. Only fields given in the request are updated.
        """
        data = request.json

        user = get_user(_email)
        if not user:
            raise wz.NotFound(f"User with email {_email} not found.")

        try:
            updated_user = users.update_user(
                email=_email,
                name=data.get("name"),
                role=data.get("role"),
                affiliation=data.get("affiliation"),
            )

            return {"message": "User updated successfully", "updated_user": updated_user}, HTTPStatus.OK
        except ValueError as e:
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST
