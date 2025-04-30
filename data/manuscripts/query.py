import data.db_connect as dbc
import data.manuscripts.fields as flds
from data.manuscripts.fields import STATE
from bson import ObjectId

# states:
COPY_EDIT = 'CED'
IN_REF_REVIEW = 'REV'
AUTHOR_REVISIONS = 'AUR'
SUBMITTED = 'SUB'
REJECTED = 'REJ'
WITHDRAWN = 'WIT'
IN_EDITOR_REVIEW = 'ERW'
IN_AUTHOR_REVIEW = 'ARW'
FORMATTING = 'FMT'
PUBLISHED = 'PUB'
# used for testing
TEST_STATE = SUBMITTED
TEST_ID = 'fake_id'
IN_REF_REV = 'REV'

# a list of valid states
VALID_STATES = [
    AUTHOR_REVISIONS,
    COPY_EDIT,
    IN_REF_REVIEW,
    REJECTED,
    SUBMITTED,
    WITHDRAWN,
    IN_EDITOR_REVIEW,
    IN_AUTHOR_REVIEW,
    FORMATTING,
    PUBLISHED,
]


def get_states() -> list:
    return VALID_STATES


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


# actions:
SUBMITTED = 'SUB'
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DELETE_REF = 'DRF'
DONE = 'DON'
REJECT = 'REJ'
WITHDRAW = 'WIT'
# used for testing:
TEST_ACTION = SUBMITTED

# a list of valid actions
VALID_ACTIONS = [
    SUBMITTED,
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    DONE,
    REJECT,
    WITHDRAW,
]

# Collection name for manuscripts
MANUSCRIPT_COLLECT = 'manuscript'


def assign_ref(manu: dict, ref: str, extra=None) -> str:
    """
    Assign a referee to a manuscript and update in database.
    
    :param manu: manuscript id
    :param ref: the name of the referee
    :param extra: extra fields to assign
    """
    if ref not in manu.get(flds.REFEREES, []):
        if flds.REFEREES in manu:
            manu[flds.REFEREES].append(ref)
        else:
            manu[flds.REFEREES] = [ref]
        update_manuscript(manu["_id"], {flds.REFEREES: manu[flds.REFEREES]})
    return IN_REF_REVIEW


def delete_ref(manu: dict, ref: str) -> str:
    """
    Remove a referee from a manuscript and update in database.
    """
    if ref in manu[flds.REFEREES]:
        manu[flds.REFEREES].remove(ref)
        update_manuscript(manu["_id"], {flds.REFEREES: manu[flds.REFEREES]})

    if len(manu[flds.REFEREES]) > 0:
        return IN_REF_REVIEW
    else:
        return SUBMITTED


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


FUNC = 'f'


COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda **kwargs: WITHDRAWN,
    },
}


STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        **COMMON_ACTIONS,
    },
    IN_REF_REVIEW: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        **COMMON_ACTIONS,
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: IN_AUTHOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVISIONS: {
        DONE: {
            FUNC: lambda **kwargs: IN_EDITOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    IN_EDITOR_REVIEW: {
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        **COMMON_ACTIONS,
    },
    IN_AUTHOR_REVIEW: {
        DONE: {
            FUNC: lambda **kwargs: FORMATTING,
        },
        **COMMON_ACTIONS,
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda **kwargs: PUBLISHED,
        },
        **COMMON_ACTIONS,
    },
    PUBLISHED: {
        **COMMON_ACTIONS,
    },
    REJECTED: {
        **COMMON_ACTIONS,
    },
    WITHDRAWN: {
        **COMMON_ACTIONS,
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def get_manuscript(manu_id: str) -> dict:
    """
    Retrieve a specific manuscript by MongoDB _id.
    """
    try:
        object_id = ObjectId(manu_id)  # Convert string to ObjectId
    except Exception:
        raise ValueError(f'Invalid MongoDB ObjectId: {manu_id}')

    manuscript = dbc.fetch_one(MANUSCRIPT_COLLECT, {"_id": object_id})
    return manuscript


def get_all_manuscripts() -> list:
    """
    Retrieve all manuscripts from the database.
    """
    return dbc.read(MANUSCRIPT_COLLECT)


def create_manuscript(
    title: str,
    author: str,
    abstract: str,
    content: str,
    submission_date: str = None,
    state: str = SUBMITTED,
) -> dict:
    """
    Create a new manuscript entry in the database.
    """
    new_manuscript = {
        "_id": ObjectId(),
        flds.TITLE: title,
        flds.AUTHOR: author,
        flds.ABSTRACT: abstract,
        flds.CONTENT: content,
        flds.SUBMISSION_DATE: submission_date,
        flds.STATE: state,
    }
    result = dbc.create(MANUSCRIPT_COLLECT, new_manuscript)

    new_manuscript["_id"] = result.inserted_id
    return new_manuscript


def update_manuscript(manu_id: str, updates: dict) -> dict:
    """
    Update a manuscript in the database using MongoDB _id.
    """
    manuscript = get_manuscript(manu_id)
    if not manuscript:
        raise ValueError(f'Manuscript with _id "{manu_id}" not found')

    dbc.update_doc(MANUSCRIPT_COLLECT, {"_id": ObjectId(manu_id)}, updates)


def delete_manuscript(manu_id: str) -> bool:
    """
    Delete a manuscript by MongoDB _id.
    """
    try:
        object_id = ObjectId(manu_id)
    except Exception:
        raise ValueError(f'Invalid MongoDB ObjectId: {manu_id}')

    result = dbc.delete(MANUSCRIPT_COLLECT, {"_id": object_id})
    return result > 0


def withdraw_manuscript(manu_id: str):
    """
    Withdraw a manuscript using MongoDB _id.
    """
    manuscript = get_manuscript(manu_id)
    if not manuscript:
        raise ValueError(f'Manuscript with _id "{manu_id}" not found')

    dbc.update_doc(MANUSCRIPT_COLLECT, {"_id": ObjectId(manu_id)}, {STATE: WITHDRAWN})


def handle_action(curr_state, action, **kwargs) -> str:
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)
