import data.db_connect as dbc
import data.manuscripts.fields as flds
from data.manuscripts.fields import CURR_STATE

# states:
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
AUTHOR_REV = 'AUR'
SUBMITTED = 'SUB'
REJECTED = 'REJ'
WITHDRAWN = 'WIT'
EDITOR_REV = 'EDR'
FORMATTING = 'FMT'
# used for testing
TEST_STATE = SUBMITTED

# a list of valid states
VALID_STATES = [
    AUTHOR_REV,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    WITHDRAWN,
    EDITOR_REV,
    FORMATTING,
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
    """
    if ref not in manu[flds.REFEREES]:
        manu[flds.REFEREES].append(ref)
        update_manuscript(manu[flds.TITLE], {flds.REFEREES: manu[flds.REFEREES]})
    return IN_REF_REV


def delete_ref(manu: dict, ref: str) -> str:
    """
    Remove a referee from a manuscript and update in database.
    """
    if ref in manu[flds.REFEREES]:
        manu[flds.REFEREES].remove(ref)
        update_manuscript(manu[flds.TITLE], {flds.REFEREES: manu[flds.REFEREES]})

    if len(manu[flds.REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


def handle_action(curr_state, action) -> str:
    if not is_valid_state(curr_state):
        raise ValueError(f'Invalid state: {curr_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')
    new_state = curr_state
    if curr_state == SUBMITTED:
        if action == ASSIGN_REF:
            new_state = IN_REF_REV
        elif action == REJECT:
            new_state = REJECTED
    elif curr_state == IN_REF_REV:
        if action == ACCEPT:
            new_state = COPY_EDIT
        elif action == REJECT:
            new_state = REJECTED
    return new_state


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
    IN_REF_REV: {
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
            FUNC: lambda **kwargs: AUTHOR_REV,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REV: {
        **COMMON_ACTIONS,
    },
    EDITOR_REV: {

    },
    FORMATTING: {

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


def get_manuscript(title: str) -> dict:
    """
    Retrieve a specific manuscript by title from the database.
    """
    return dbc.fetch_one(MANUSCRIPT_COLLECT, {flds.TITLE: title})


def get_all_manuscripts() -> list:
    """
    Retrieve all manuscripts from the database.
    """
    return dbc.read(MANUSCRIPT_COLLECT)


def create_manuscript(
    title: str,
    author: str,
    content: str,
    publication_date: str = None,
    state: str = SUBMITTED,
) -> dict:
    """
    Create a new manuscript entry in the database.
    """
    new_manuscript = {
        flds.TITLE: title,
        flds.AUTHOR: author,
        flds.CONTENT: content,
        flds.PUBLICATION_DATE: publication_date,
        flds.CURR_STATE: state,
    }
    existing = get_manuscript(title)
    if existing:
        raise ValueError(f'Manuscript with title "{title}" already exists')

    dbc.create(MANUSCRIPT_COLLECT, new_manuscript)
    return new_manuscript


def update_manuscript(title: str, updates: dict) -> dict:
    """
    Update a manuscript in the database.
    """
    manuscript = get_manuscript(title)
    if not manuscript:
        raise ValueError(f'Manuscript with title "{title}" not found')
    if '_id' in updates:
        del updates['_id']
    dbc.update_doc(MANUSCRIPT_COLLECT, {flds.TITLE: title}, updates)


def delete_manuscript(title: str) -> bool:
    """
    Delete a manuscript by title from a simulated database.
    """
    result = dbc.delete(MANUSCRIPT_COLLECT, {flds.TITLE: title})
    return result > 0

def withdraw_manuscript(title: str):
    """
    Withdraws a manuscript by title. Requires the user to be the author of the manuscript.
    """
    manuscript = get_manuscript(title)
    if not manuscript:
        raise ValueError(f'Manuscript with title "{title}" not found')
    
    # TODO: user has to be the author
    dbc.update_doc(MANUSCRIPT_COLLECT, {flds.TITLE: title}, {CURR_STATE: WITHDRAW})
