"""
This is the file containing all the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

import werkzeug.exceptions as wz
from flask import Flask, request  # , reques
from flask_cors import CORS
from flask_restx import Resource, Api, fields  # Namespace, fields

import data.roles as rls
import data.text as text
import data.users as users
from data.manuscripts import fields as manuscript_fields
from data.manuscripts import query as manuscript_query
from data.text import read_texts, read_one, create, update, delete, KEY, TITLE, TEXT
from data.users import get_user, NAME, EMAIL, AFFILIATION, ROLE, ROLES

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = "/endpoints"
ENDPOINT_RESP = "Available endpoints"
HELLO_EP = "/hello"
HELLO_RESP = "hello"
TITLE_EP = "/title"
TITLE_RESP = "Title"
EDITOR_RESP = "Editor"
EDITOR = "ejc369@nyu.edu"
DATE_RESP = "Date"
DATE = "2024-09-24"
JOURNAL_NAME_EP = "/journal-name"
JOURNAL_NAME_RESP = "Journal Name"
JOURNAL_NAME = "wema"
USERS_EP = "/users"
USERS = users.get_users_as_dict()
TEXT_EP = "/text"
MANUSCRIPTS_EP = "/manuscripts"
ROLES_EP = '/roles'

USER_CREATE_FIELDS = api.model('AddNewUserEntry', {
    users.NAME: fields.String(required=True, description="User's name"),
    users.EMAIL: fields.String(required=True, description="User's email"),
    users.AFFILIATION: fields.String(required=True, description="User's affiliation"),
    users.ROLE: fields.String(description="User's role"),
})

USER_UPDATE_FIELDS = api.model('UpdateUserEntry', {
    users.NAME: fields.String(description="User's name"),
    users.EMAIL: fields.String(description="User's email"),
    users.AFFILIATION: fields.String(description="User's affiliation"),
    users.ROLE: fields.String(description="User's role"),
})

TEXT_CREATE_FIELDS = api.model('AddNewTextEntry', {
    text.KEY: fields.String(required=True, description="Unique key for the text"),
    text.TITLE: fields.String(required=True, description="Title of the text"),
    text.TEXT: fields.String(required=True, description="Content of the text"),
})

TEXT_UPDATE_FIELDS = api.model('UpdateTextEntry', {
    text.TITLE: fields.String(description="Title of the text"),
    text.TEXT: fields.String(description="Content of the text"),
})

MANUSCRIPT_CREATE_FIELDS = api.model('AddNewManuscriptEntry', {
    manuscript_fields.TITLE: fields.String(required=True, description="Manuscript's title"),
    manuscript_fields.AUTHOR: fields.String(required=True, description="Manuscript's author"),
    manuscript_fields.CONTENT: fields.String(required=True, description="Manuscript's content"),
    manuscript_fields.PUBLICATION_DATE: fields.String(description="Publication date of the manuscript"),
})

MANUSCRIPT_UPDATE_FIELDS = api.model('UpdateManuscriptEntry', {
    manuscript_fields.TITLE: fields.String(description="Manuscript's title"),
    manuscript_fields.AUTHOR: fields.String(description="Author's name"),
    manuscript_fields.CONTENT: fields.String(description="Manuscript content"),
    manuscript_fields.PUBLICATION_DATE: fields.String(description="Publication date"),
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
        If email query parameter is provided, return specific user.
        """
        email = request.args.get(EMAIL)
        if email:
            # Search through the users list for the matching email
            users_list = users.get_users()  # This will use our mocked data
            for user in users_list:
                if user.email == email:
                    return {email: user.to_dict()}
            return {"message": f"User {email} not found"}, HTTPStatus.NOT_FOUND
        return users.get_users_as_dict()

    @api.expect(USER_CREATE_FIELDS)
    @api.response(HTTPStatus.CREATED, "User created successfully")
    @api.response(HTTPStatus.BAD_REQUEST, "Invalid data provided")
    def post(self):
        """
        Adds a new user with given JSON data
        """
        data = request.json
        required_fields = [NAME, EMAIL, AFFILIATION]

        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, HTTPStatus.BAD_REQUEST

        try:
            users.create_user(
                name=data[NAME],
                email=data[EMAIL],
                role=data[ROLE] if ROLE in data else None,
                affiliation=data[AFFILIATION],
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
        """
        Retrieve a specific user by email
        """
        user = get_user(_email)
        if not user:
            return {"message": f"User {_email} not found"}, HTTPStatus.NOT_FOUND

        user_dict = user.to_dict()

        # Make sure the roles list contains the role if it exists
        if not user_dict.get(ROLES):
            user_dict[ROLES] = []

        if ROLE in request.args:
            role = request.args.get(ROLE)
            if role not in user_dict[ROLES]:
                user_dict[ROLES].append(role)

        return user_dict

    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "No such person")
    def delete(self, _email):
        """
        Delete a user by email
        """
        ret = users.delete_user(_email)
        if ret is not None:
            return {"Deleted": ret.to_dict()}, HTTPStatus.OK
        return {"message": f"User {_email} not found"}, HTTPStatus.NOT_FOUND

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
                name=data.get(NAME),
                role=data.get(ROLE),
                affiliation=data.get(AFFILIATION),
            )

            return {"message": "User updated successfully", "updated_user": updated_user}, HTTPStatus.OK
        except ValueError as e:
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST


@api.route(TEXT_EP)
class Texts(Resource):
    """
    This class handles creating and reading multiple texts.
    """

    def get(self):
        """
        Retrieve all texts.
        """
        return read_texts(), HTTPStatus.OK

    @api.expect(TEXT_CREATE_FIELDS)
    @api.response(HTTPStatus.CREATED, "Text created successfully")
    @api.response(HTTPStatus.BAD_REQUEST, "Invalid data provided")
    def post(self):
        """
        Create a new text entry.
        """
        data = request.json
        key = data.get(KEY)
        title = data.get(TITLE)
        content = data.get(TEXT)

        if not key or not title or not content:
            return {"message": "Missing required fields"}, HTTPStatus.BAD_REQUEST

        try:
            created_text = create(key=key, title=title, text=content)
            return {"message": "Text created successfully", "text": created_text}, HTTPStatus.CREATED
        except ValueError as ve:
            return {"message": str(ve)}, HTTPStatus.CONFLICT
        except Exception:
            return {"message": "An error occurred while creating the text "}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route(f"{TEXT_EP}/<string:key>")
class SingleText(Resource):
    """
    This class handles reading, updating, and deleting a single text.
    """

    def get(self, key):
        """
        Retrieve a specific text by key.
        """
        text_entry = read_one(key)
        if not text_entry:
            return {"message": f"Text with key '{key}' not found"}, HTTPStatus.NOT_FOUND

        return text_entry, HTTPStatus.OK

    @api.expect(TEXT_UPDATE_FIELDS)
    @api.response(HTTPStatus.OK, "Text updated successfully")
    @api.response(HTTPStatus.NOT_FOUND, "Text not found")
    @api.response(HTTPStatus.BAD_REQUEST, "Invalid data provided")
    def patch(self, key):
        """
        Update a specific text by key.
        """
        data = request.json
        title = data.get(TITLE)
        content = data.get(TEXT)

        try:
            updated_text = update(key=key, title=title, text=content)
            return {"message": "Text updated successfully", "text": updated_text}, HTTPStatus.OK
        except ValueError as e:
            return {"message": str(e)}, HTTPStatus.NOT_FOUND

    def delete(self, key):
        """
        Delete a specific text by key.
        """
        deleted_text = delete(key)
        if not deleted_text:
            return {"message": f"Text with key '{key}' not found"}, HTTPStatus.NOT_FOUND

        return {"message": "Text deleted successfully", "deleted_text": deleted_text}, HTTPStatus.OK


@api.route(MANUSCRIPTS_EP)
class Manuscripts(Resource):
    """
    This class handles creating, reading, updating, and deleting manuscripts.
    """

    def get(self):
        """
        Retrieve the list of manuscripts.
        If a title query parameter is provided, return specific manuscript.
        """
        return manuscript_query.get_all_manuscripts()

    @api.expect(MANUSCRIPT_CREATE_FIELDS)
    @api.response(HTTPStatus.CREATED, "Manuscript created successfully")
    @api.response(HTTPStatus.BAD_REQUEST, "Invalid data provided")
    def post(self):
        """
        Adds a new manuscript with given JSON data
        """
        data = request.json
        required_fields = [manuscript_fields.TITLE, manuscript_fields.AUTHOR, manuscript_fields.CONTENT]

        if not all(field in data for field in required_fields):
            return {"message": "Missing required fields"}, HTTPStatus.BAD_REQUEST

        try:
            manuscript_query.create_manuscript(
                title=data[manuscript_fields.TITLE],
                author=data[manuscript_fields.AUTHOR],
                content=data[manuscript_fields.CONTENT],
                publication_date=data.get(manuscript_fields.PUBLICATION_DATE, None),
            )
            return {"message": "Manuscript added successfully!", "added_manuscript": data}, HTTPStatus.CREATED
        except ValueError as e:
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST


@api.route(f"{MANUSCRIPTS_EP}/<string:title>")
class Manuscript(Resource):
    """
    This class handles reading, updating, and deleting a single manuscript.
    """

    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Manuscript not found")
    def get(self, title):
        """
        Retrieve a specific manuscript by title.
        """
        manuscript = manuscript_query.get_manuscript(title)
        if not manuscript:
            return {"message": f"Manuscript with title '{title}' not found"}, HTTPStatus.NOT_FOUND
        return manuscript, HTTPStatus.OK

    @api.expect(MANUSCRIPT_UPDATE_FIELDS)
    @api.response(HTTPStatus.OK, "Manuscript updated successfully")
    @api.response(HTTPStatus.NOT_FOUND, "Manuscript not found")
    @api.response(HTTPStatus.BAD_REQUEST, "Invalid data provided")
    def patch(self, title):
        """
        Update a manuscript. Only fields provided in the request are updated.
        """
        data = request.json
        manuscript = manuscript_query.get_manuscript(title)
        if not manuscript:
            return {"message": f"Manuscript with title '{title}' not found"}, HTTPStatus.NOT_FOUND

        for field in [manuscript_fields.TITLE, manuscript_fields.AUTHOR, manuscript_fields.CONTENT,
                      manuscript_fields.PUBLICATION_DATE]:
            if field in data:
                manuscript[field] = data[field]

        try:
            manuscript_query.update_manuscript(title, manuscript)
            return {"message": "Manuscript updated successfully"}, HTTPStatus.OK
        except ValueError as e:
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST

    @api.response(HTTPStatus.OK, "Manuscript deleted successfully")
    @api.response(HTTPStatus.NOT_FOUND, "Manuscript not found")
    def delete(self, title):
        """
        Delete a manuscript by title.
        """
        success = manuscript_query.delete_manuscript(title)
        if success:
            return {"message": f"Manuscript '{title}' deleted successfully"}, HTTPStatus.OK
        return {"message": f"Manuscript '{title}' not found"}, HTTPStatus.NOT_FOUND


# Finite State Machine
MANU_ACTION_FLDS = api.model('ManuscriptAction', {
    manuscript_fields.TITLE: fields.String,
    manuscript_fields.STATE: fields.String,
    manuscript_fields.ACTION: fields.String,
})


@api.route(f'{MANUSCRIPTS_EP}/receive_action')
class ReceiveAction(Resource):
    """
    Receive an action for a manuscript.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_ACTION_FLDS)
    def put(self):
        """
        Receive an action for a manuscript.
        """
        try:
            title = request.json.get(manuscript_fields.TITLE)
            curr_state = request.json.get(manuscript_fields.STATE)
            action = request.json.get(manuscript_fields.ACTION)
            kwargs = {k: v for k, v in request.json.items() if k not in [
                        manuscript_fields.TITLE,
                        manuscript_fields.STATE,
                        manuscript_fields.ACTION
                    ]}
            manu = manuscript_query.get_manuscript(title)
            manuscript_query.handle_action(curr_state, action, manu=manu, **kwargs)
            return {'message': 'Action processed successfully'}, HTTPStatus.OK
        except Exception as err:
            raise wz.NotAcceptable(f'Bad action: {err=}')


@api.route(ROLES_EP)
class Roles(Resource):
    """
    This class handles reading person roles.
    """
    def get(self):
        """
        Retrieve the journal person roles.
        """
        return rls.read()
