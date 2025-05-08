from functools import wraps
from logging import Logger
import time
from data.roles import Role

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
LOGIN_KEY = 'login_key'
IP_ADDR = 'ip_address'
MFA = 'mfa'
ROLE_LIST = 'role_list'

# Features:
PEOPLE = 'people'
BAD_FEATURE = 'baaaad feature'

PEOPLE_MISSING_ACTION = READ
GOOD_USER_ID = 'ed2303@nyu.edu'

security_recs = None

PEOPLE = 'people'
TEXTS = 'texts'
BAD_FEATURE = 'baaaad feature'
PEOPLE_MISSING_ACTION = READ
GOOD_USER_ID = 'wl2612@nyu.edu'

ALL_ROLES = [role.value for role in Role]
EDITORS = [Role.EDITOR.value, Role.CONSULTING_EDITOR.value, Role.MANAGING_EDITOR.value]
CREATORS = [Role.AUTHOR.value, Role.EDITOR.value, Role.CONSULTING_EDITOR.value, Role.MANAGING_EDITOR.value]

ADMINS = {
    ROLE_LIST: [Role.EDITOR.value, Role.CONSULTING_EDITOR.value, Role.MANAGING_EDITOR.value],
    CHECKS: {
        LOGIN: True,
    },
}

TEST_RECS = {
    PEOPLE: {
        CREATE: ALL_ROLES,
        READ: ALL_ROLES,
        DELETE: ADMINS,
        UPDATE: ADMINS,
    },
    TEXTS: {
        CREATE: {
            ROLE_LIST: ALL_ROLES,
            CHECKS: {
                LOGIN: True,
            },
        },
        UPDATE: {
            ROLE_LIST: CREATORS,
            CHECKS: {
                LOGIN: True,
            },
        },
        READ: {
            ROLE_LIST: ALL_ROLES,
            CHECKS: {
                LOGIN: True,
            },
        },
        DELETE: {
            ROLE_LIST: ADMINS,
            CHECKS: {
                LOGIN: True,
                IP_ADDR: True,
                MFA: True,
            },
        },
    },
    BAD_FEATURE: {
        CREATE: {
            ROLE_LIST: ALL_ROLES,
            CHECKS: {
                'Bad check': True,
            },
        },
    },
}


def is_valid_key(user_id: str, login_key: str):
    """
    This is just a mock of the real is_valid_key() we'll write later.
    """
    return True


def check_login(user_roles: list, **kwargs):
    if LOGIN_KEY not in kwargs:
        return False
    return is_valid_key("dummy_user", kwargs[LOGIN_KEY])


CHECK_FUNCS = {
    LOGIN: check_login,
    # IP_ADDRESS: check_ip,
 }


def read() -> dict:
    global security_recs
    # dbc.read()
    security_recs = TEST_RECS
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


"""@needs_recs
def is_permitted(feature_name: str, action: str, user_id: str, **kwargs) -> bool:
    prot = read_feature(feature_name)
    if prot is None:
        return True
    if action not in prot:
        return True
    if USER_LIST in prot[action]:
        if user_id not in prot[action][USER_LIST]:
            return False
    if CHECKS not in prot[action]:
        return True
    for check in prot[action][CHECKS]:
        if check not in CHECK_FUNCS:
            raise ValueError(f'Bad check passed to is_permitted: {check}')
        if not CHECK_FUNCS[check](user_id, **kwargs):
            return False
    return True"""


@needs_recs
def is_permitted(feature_name: str, action: str, user_roles: list, **kwargs) -> bool:
    """Check if operation on feature is permitted for roles."""
    prot = read_feature(feature_name)
    if prot is None or not user_roles:
        return False
    if action not in prot:
        return False
    # Role check
    if ROLE_LIST in prot[action]:
        if not any(role in prot[action][ROLE_LIST] for role in user_roles):
            return False
    # Check for invalid check functions before executing any
    if CHECKS in prot[action]:
        for check_name in prot[action][CHECKS]:
            if check_name not in CHECK_FUNCS:
                # This should raise the ValueError
                raise ValueError(f'Bad check passed to is_permitted: {check_name}')
        # Now execute valid checks
        for check_name, is_required in prot[action][CHECKS].items():
            if is_required and not CHECK_FUNCS[check_name](user_roles, **kwargs):
                return False
    return True


@needs_recs
def get_user_permissions(user_email: str) -> dict:
    """
    Get all permissions for a specific user.
    Args:
        user_email: The email of the user

    Returns:
        dict: A dictionary of features and operations the user has access to
    """
    result = {}
    for feature_name, feature_data in security_recs.items():
        feature_perms = {}
        for operation, op_data in feature_data.items():
            if USER_LIST in op_data and user_email in op_data[USER_LIST]:
                feature_perms[operation] = True
        if feature_perms:
            result[feature_name] = feature_perms
    return result


def get_feature_permissions(feature_name: str) -> dict:
    """
    Get all permissions for a specific feature.
    Args:
        feature_name: The name of the feature

    Returns:
        dict: A dictionary of operations and users with access
    """
    if feature_name not in security_recs:
        return {}
    return security_recs[feature_name]


@needs_recs
def get_role_permissions(role: str) -> dict:
    """
    Get all permissions for a specific role.
    Args:
        role: The role to check permissions for

    Returns:
        dict: A dictionary of features and operations the role has access to
    """
    result = {}
    for feature_name, feature_data in security_recs.items():
        feature_perms = {}
        for operation, op_data in feature_data.items():
            if ROLE_LIST in op_data and role in op_data[ROLE_LIST]:
                feature_perms[operation] = True
        if feature_perms:
            result[feature_name] = feature_perms
    return result


# Role-based Access Control Security Feature

DELETE_PERMISSIONS = {
    ROLE_LIST: EDITORS,
    CHECKS: {
        LOGIN: True,
    },
}

CREATE_PERMISSIONS = {
    ROLE_LIST: ALL_ROLES,
    CHECKS: {
        LOGIN: True,
    },
}

READ_PERMISSIONS = {
    ROLE_LIST: ALL_ROLES,
    CHECKS: {
        LOGIN: True,
    },
}

UPDATE_PERMISSIONS = {
    ROLE_LIST: CREATORS,
    CHECKS: {
        LOGIN: True,
    },
}

TEST_RECS = {
    PEOPLE: {
        CREATE: CREATE_PERMISSIONS,
        READ: READ_PERMISSIONS,
        UPDATE: UPDATE_PERMISSIONS,
        DELETE: DELETE_PERMISSIONS,
    },
    TEXTS: {
        CREATE: CREATE_PERMISSIONS,
        READ: READ_PERMISSIONS,
        UPDATE: UPDATE_PERMISSIONS,
        DELETE: DELETE_PERMISSIONS,
    },
}
