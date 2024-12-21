import data.db_connect as dbc

KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

COLLECTION = 'texts'

client = dbc.connect_db()
print(f'{client=}')


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    try:
        db_texts = dbc.read(COLLECTION)
        return {text[KEY]: {TITLE: text.get(TITLE, ""), TEXT: text.get(TEXT, "")} for text in db_texts}
    except Exception as e:
        print(f"Error reading texts: {e}")
        return {}


def read_one(key: str) -> dict:
    """
    Read a single text entry by key.
    Returns empty dict if not found.
    """
    try:
        db_text = dbc.fetch_one(COLLECTION, {KEY: key})
        # Just check if document exists for duplicate check
        return not not db_text  # Converts to boolean
    except Exception as e:
        print(f"Error reading text with key '{key}': {e}")
        return False


def create(key: str, title: str, text: str):
    """
    Create a new text entry in the database.
    """
    try:
        if read_one(key):
            raise ValueError(f"Text with key '{key}' already exists.")

        new_entry = {
            KEY: str(key),
            TITLE: str(title),
            TEXT: str(text)
        }
        dbc.create(COLLECTION, new_entry)
        return {KEY: str(key), TITLE: str(title), TEXT: str(text)}
    except Exception as e:
        print(f"Error creating text: {e}")
        raise


def delete(key):
    """
    Delete a text entry from the database.
    """
    try:
        result = dbc.delete(COLLECTION, {KEY: key})
        return result > 0
    except Exception as e:
        print(f"Error deleting text with key '{key}': {e}")
        return False


def update(key, title=None, text=None):
    """
    Update an existing text entry in the database.
    """
    try:
        if not read_one(key):
            raise ValueError(f"Text with key '{key}' does not exist.")

        updates = {}
        if title:
            updates[TITLE] = title
        if text:
            updates[TEXT] = text

        if not updates:
            raise ValueError("No updates provided.")

        dbc.update_doc(COLLECTION, {KEY: key}, updates)
        updated_entry = read_one(key)
        return updated_entry
    except Exception as e:
        print(f"Error updating text with key '{key}': {e}")
        raise
