
TITLE = 'title'
DISPLAY_NAME = 'display_name'

TEST_FLD_NM = TITLE
TEST_FLD_DISPLAY_NM = 'Title'


FIELDS = {
    TITLE: {
        DISPLAY_NAME: TEST_FLD_DISPLAY_NM,
    },
}


def get_fields() -> dict:
    return FIELDS


def get_field_names() -> list:
    return FIELDS.keys()