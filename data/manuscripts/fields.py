TITLE = 'title'
AUTHOR = 'author'
DISPLAY_NAME = 'display_name'
REFEREES = 'ref'
CONTENT = 'content'
SUBMISSION_DATE = 'submission_date'

#FSM 
STATE = 'state'
ACTION = 'action'

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
    return list(FIELDS.keys())


def get_disp_name(fld_nm: str) -> dict:
    fld = FIELDS.get(fld_nm, '')
    return fld[DISPLAY_NAME] 


def main():
    print(f'{get_fields()=}')


if __name__ == '__main__':
    main()