import random

import pytest

import data.manuscripts.query as mqry
import data.manuscripts.fields as flds


def gen_random_not_valid_str() -> str:
    """
    That huge number is only important in being huge:
        any big number would do.
    """
    BIG_NUM = 10_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    bad_str = str(big_int)
    return bad_str


def test_is_valid_state():
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)


def test_is_not_valid_state():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_state(gen_random_not_valid_str())


def test_is_valid_action():
    for action in mqry.get_actions():
        assert mqry.is_valid_action(action)


def test_is_not_valid_action():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_action(gen_random_not_valid_str())


def test_handle_action_bad_state():
    with pytest.raises(ValueError):
        mqry.handle_action(gen_random_not_valid_str(),
                           mqry.TEST_ACTION)


def test_handle_action_bad_action():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_STATE,
                           gen_random_not_valid_str())


def test_handle_action_valid_return():
    SAMPLE_MANU = mqry.create_manuscript(
        title='the title of test',
        author='John Doe',
        abstract='abstract goes here',
        content='content goes here',
        submission_date='today',
    )
    try:
        manu_id = str(SAMPLE_MANU["_id"])
        assert manu_id is not None

        for state in mqry.get_states():
            for action in mqry.get_valid_actions_by_state(state):
                new_state = mqry.handle_action(state, action, manu=SAMPLE_MANU, ref="a referee")
                assert mqry.is_valid_state(new_state)

    finally:
        mqry.delete_manuscript(manu_id)
