KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEST_KEY = 'HomePage'
SUBM_KEY = 'SubmissionsPage'
DEL_KEY = 'DeletePage'

text_dict = {
    TEST_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
    SUBM_KEY: {
        TITLE: 'Submissions Page',
        TEXT: 'All submissions must be original work in Word format.',
    },
    DEL_KEY: {
        TITLE: 'Delete Page',
        TEXT: 'This is a text to delete.',
    },
}


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = text_dict
    return text


def create(key, title, text):
    if key in text_dict:
        raise ValueError(f"Text with key '{key}' already exists.")
    text_dict[key] = {TITLE: title, TEXT: text}
    return text_dict[key]


def delete(key):
    return text_dict.pop(key, None)


def update(key, title=None, text=None):
    if key not in text_dict:
        raise ValueError(f"Text with key '{key}' does not exist.")
    if title:
        text_dict[key][TITLE] = title
    if text:
        text_dict[key][TEXT] = text
    return text_dict[key]


if __name__ == '__main__':
    pass
