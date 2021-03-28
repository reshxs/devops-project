import pytest

from auth.utils import hash_password, match_password
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
