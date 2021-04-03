import pytest

from auth.utils import hash_password, match_password, email_is_valid
from auth.models import User


@pytest.mark.parametrize("test_input, expected", [
    ("password", True),
    ("wrong_pwd", False),
    (" ", False),
    ("", False)
])
def test_match_password(test_input, expected):
    pwd = 'password'
    user = User()
    user.user_password = hash_password(pwd)
    assert match_password(user, eval("test_input")) == expected


@pytest.mark.parametrize("test_input, expected", [
    ('test@example.com', True),
    ('test.test@exmample.com', True),
    ('', False),
    ('test.example.com', False)
])
def test_email_validation(test_input, expected):
    assert email_is_valid(test_input) == expected


def test_login(client):
    # todo: Implement test
    assert False, "Implement this test"


def test_login_when_user_does_not_exists(client):
    # todo: Implement test
    assert False, "Implement this test"


def test_login_when_password_is_wrong(client):
    # todo: Implement test
    assert False, "Implement this test"


def test_register(client):
    # todo: Implement test
    assert False, "Implement this test"
