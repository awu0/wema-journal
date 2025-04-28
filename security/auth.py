"""
This module provides authentication routes for the application.
"""

import jwt
import datetime
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import data.users as users

# Create a Blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
# Generate a secure random secret key if none is provided
# This will be different each time the app restarts - in production you'd want to store this
SECRET_KEY = str(uuid.uuid4())
JWT_EXPIRATION_DELTA = datetime.timedelta(days=1)  # Token expires in 1 day


def generate_token(email):
    """
    Generate a JWT token for the given email
    """
    payload = {
        'exp': datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA,
        'iat': datetime.datetime.utcnow(),
        'sub': email
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    # Check if required fields are present
    if not all(k in data for k in ('name', 'email', 'password', 'affiliation')):
        return jsonify({'message': 'Missing required fields!'}), 400
    # Check if email is valid
    if not users.is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format!'}), 400
    # Check if user already exists
    existing_user = users.get_user(data['email'])
    if existing_user:
        return jsonify({'message': 'Email already exists!'}), 409
    # Hash the password
    hashed_password = generate_password_hash(data['password'])
    # Create a new user with the hashed password
    # Store the hashed password in a new collection or update your User class
    # For now, we'll use your existing create_user function and store the password separately
    try:
        # Create the user without password in the User collection
        users.create_user(
            name=data['name'],
            email=data['email'],
            affiliation=data['affiliation']
        )
        # Store the password in a separate auth collection
        from data.db_connect import create
        create('auth', {
            'email': data['email'],
            'password': hashed_password
        })
        # Generate JWT token
        token = generate_token(data['email'])
        # Get the created user
        new_user = users.get_user(data['email'])
        return jsonify({
            'message': 'User created successfully!',
            'token': token,
            'user': new_user.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Check if required fields are present
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'message': 'Missing required fields!'}), 400
    # Find user by email
    user = users.get_user(data['email'])
    if not user:
        return jsonify({'message': 'Invalid email or password!'}), 401
    # Get the stored password hash from the auth collection
    from data.db_connect import read_one
    auth_record = read_one('auth', {'email': data['email']})
    if not auth_record or not check_password_hash(auth_record['password'], data['password']):
        return jsonify({'message': 'Invalid email or password!'}), 401
    # Generate JWT token
    token = generate_token(data['email'])
    return jsonify({
        'message': 'Login successful!',
        'token': token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Token is missing!'}), 401
    token = auth_header.split(' ')[1]
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        email = payload['sub']
        # Get user
        user = users.get_user(email)
        if not user:
            return jsonify({'message': 'User not found!'}), 404
        return jsonify(user.to_dict()), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


# Function to require authentication for other routes
def token_required(f):
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Token is missing!'}), 401
        token = auth_header.split(' ')[1]
        try:
            # Decode token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            email = payload['sub']
            # Get user
            current_user = users.get_user(email)
            if not current_user:
                return jsonify({'message': 'User not found!'}), 404
            return f(current_user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
    decorated.__name__ = f.__name__
    return decorated
