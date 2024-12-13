import data.manuscripts.fields as flds

# states:
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
AUTHOR_REV = 'AUR'
SUBMITTED = 'SUB'
REJECTED = 'REJ'
WITHDRAWN = 'WIT'
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
]

SAMPLE_MANU = {
    flds.TITLE: 'Short module import names in Python',
    flds.AUTHOR: 'Matthew Ma',
    flds.REFEREES: [],
}


def get_states() -> list:
    return VALID_STATES


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


# actions:
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DELETE_REF = 'DRF'
DONE = 'DON'
REJECT = 'REJ'
WITHDRAW = 'WIT'
# used for testing:
TEST_ACTION = ACCEPT

# a list of valid actions
VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    DONE,
    REJECT,
    WITHDRAW,
]


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