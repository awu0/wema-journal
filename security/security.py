from functools import wraps
from logging import Logger
import time
# import data.db_connect as dbc

"""
Our record format to meet our requirements (see security.md) will be:

{
    feature_name1: {
        create: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        read: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        update: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        delete: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
    },
    feature_name2: # etc.
}
"""

COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'

# Features:
PEOPLE = 'people'

security_recs = None
# These will come from the DB soon:
temp_recs = {
    PEOPLE: {
        CREATE: {
            USER_LIST: ['ejc369@nyu.edu'],
            CHECKS: {
                LOGIN: True,
            },
        },
    },
}


def read() -> dict:
    global security_recs
    # dbc.read()
    security_recs = temp_recs
    return security_recs


def needs_recs(fn):
    """
    Should be used to decorate any function that directly accesses sec recs.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global security_recs
        if not security_recs:
            security_recs = read()
        return fn(*args, **kwargs)
    return wrapper


@needs_recs
def read_feature(feature_name: str) -> dict:
    if feature_name in security_recs:
        return security_recs[feature_name]
    else:
        return None


@needs_recs
def check_permission(feature_name: str, operation: str, user_email: str, ip_address=None) -> bool:
    """
    Check if a user has permission to perform an operation on a feature.
    Args:
        feature_name: The name of the feature
        operation: The operation (CREATE, READ, UPDATE, DELETE)
        user_email: The email of the user
        ip_address: The IP address of the user (optional)
    Returns:
        bool: True if the user has permission, False otherwise
    """
    if feature_name not in security_recs:
        Logger.warning(f"Feature '{feature_name}' not found in security records")
        return False
    if operation not in security_recs[feature_name]:
        Logger.warning(f"Operation '{operation}' not defined for feature '{feature_name}'")
        return False
    feature_sec = security_recs[feature_name][operation]
    if feature_sec[CHECKS].get(LOGIN, True) and not user_email:
        Logger.warning("Login required but no user email provided")
        return False
    if feature_sec[CHECKS].get(ip_address, False) and not ip_address:
        Logger.warning("IP address check required but no IP address provided")
        return False
    user_list = feature_sec[USER_LIST]
    if user_list and user_email not in user_list:
        Logger.warning(f"User '{user_email}' not in allow list for '{operation}' on '{feature_name}'")
        return False
    return True


def _log_audit(user_email: str, feature_name: str, operation: str) -> None:
    """
    Log an audit entry for a security-sensitive operation.
    Args:
        user_email: The email of the user
        feature_name: The name of the feature
        operation: The operation performed
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    Logger.info(f"AUDIT: {timestamp} - User '{user_email}' performed '{operation}' on '{feature_name}'")
    # In production, this would write to a secure audit log in the databased


@needs_recs
def add_user_permission(feature_name: str, operation: str, user_email: str) -> bool:
    """
    Add permission for a user to perform an operation on a feature.
    Args:
        feature_name: The name of the feature
        operation: The operation (CREATE, READ, UPDATE, DELETE)
        user_email: The email of the user

    Returns:
        bool: True if successful, False otherwise
    """
    if feature_name not in security_recs:
        security_recs[feature_name] = {}
    if operation not in security_recs[feature_name]:
        security_recs[feature_name][operation] = {
            USER_LIST: [],
            CHECKS: {
                LOGIN: True,
            },
        }
    if user_email not in security_recs[feature_name][operation][USER_LIST]:
        security_recs[feature_name][operation][USER_LIST].append(user_email)
    return  # write to database (Needs to be Implemented)


@needs_recs
def remove_user_permission(feature_name: str, operation: str, user_email: str) -> bool:
    """
    Remove permission for a user to perform an operation on a feature.
    Args:
        feature_name: The name of the feature
        operation: The operation (CREATE, READ, UPDATE, DELETE)
        user_email: The email of the user

    Returns:
        bool: True if successful, False otherwise
    """
    # Check if feature and operation exist
    if (feature_name not in security_recs or
            operation not in security_recs[feature_name] or
            USER_LIST not in security_recs[feature_name][operation]):
        return True  # Nothing to remove
    # Remove user if present
    if user_email in security_recs[feature_name][operation][USER_LIST]:
        security_recs[feature_name][operation][USER_LIST].remove(user_email)
    return  # write to database (Needs to be Implemented)
