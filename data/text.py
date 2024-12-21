import data.db_connect as dbc

KEY = 'key'
TITLE = 'title'
TEXT = 'text'

COLLECTION = 'texts'

client = dbc.connect_db()
print(f'{client=}')


def read():
    """
    Retrieve all text entries from the database.
    """
    try:
        db_texts = dbc.read(COLLECTION)
        return {text[KEY]: {TITLE: text[TITLE], TEXT: text[TEXT]} for text in db_texts}
    except Exception as e:
        print(f"Error reading texts: {e}")
        return {}


def create(key, title, text):
    """
    Create a new text entry in the database.
    """
    existing_texts = read()
    if key in existing_texts:
        raise ValueError(f"Text with key '{key}' already exists.")
    new_entry = {KEY: key, TITLE: title, TEXT: text}
    dbc.create(COLLECTION, new_entry)
    return new_entry


def delete(key):
    """
    Delete a text entry from the database.
    """
    deleted = dbc.delete(COLLECTION, {KEY: key})
    return deleted


def update(key, title=None, text=None):
    """
    Update an existing text entry in the database.
    """
    existing_texts = read()
    if key not in existing_texts:
        raise ValueError(f"Text with key '{key}' does not exist.")
    updates = {}
    if title:
        updates[TITLE] = title
    if text:
        updates[TEXT] = text
    dbc.update_doc(COLLECTION, {KEY: key}, updates)
    updated_entry = dbc.read(COLLECTION, {KEY: key})
    return updated_entry[0] if updated_entry else None
