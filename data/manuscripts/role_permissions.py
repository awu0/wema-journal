AUTHOR = 'author'
EDITOR = 'editor'
REFEREE = 'referee'

ROLE_PERMISSIONS = {
    # State: {Action: [allowed_roles]}
    'SUB': {  # Submitted
        'ARF': [EDITOR],  
        'REJ': [EDITOR],  
        'WIT': [AUTHOR], 
    },
    'REV': {  # In Referee Review
        'ARF': [EDITOR],  
        'DRF': [EDITOR],  
        'ACC': [EDITOR],  
        'ACW': [EDITOR],  
        'WIT': [AUTHOR],  
    },
    'CED': {  # Copy Edit
        'DON': [EDITOR], 
        'WIT': [AUTHOR], 
    },
    'AUR': {  # Author Revisions
        'DON': [AUTHOR], 
        'WIT': [AUTHOR], 
    },
    'ERW': {  # In Editor Review
        'ACC': [EDITOR],  
        'WIT': [AUTHOR],  
    },
    'ARW': {  # In Author Review
        'DON': [AUTHOR], 
        'WIT': [AUTHOR], 
    },
    'FMT': {  # Formatting
        'DON': [EDITOR],  
        'WIT': [AUTHOR], 
    },
    'PUB': {  # Published
        'WIT': [EDITOR], 
    },
    'REJ': {  # Rejected
        'WIT': [AUTHOR],
    },
    'WIT': {  # Withdrawn
    },
}

def can_perform_action(state, action, user_roles):
    """
    Check if a user with given roles can perform an action on a manuscript in a specific state
    
    :param state: Current state of the manuscript (e.g., 'SUB', 'REV')
    :param action: Action to perform (e.g., 'ARF', 'DON')
    :param user_roles: List of roles the user has
    :return: Boolean indicating whether the user can perform the action
    """
    if state not in ROLE_PERMISSIONS:
        return False
    
    if action not in ROLE_PERMISSIONS[state]:
        return False
    
    allowed_roles = ROLE_PERMISSIONS[state][action]
    
    return any(role in allowed_roles for role in user_roles)
