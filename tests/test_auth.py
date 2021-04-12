import random

import pytest

from auth.utils import hash_password, match_password, email_is_valid, phone_is_valid
from auth.models import User
from tests.helpers import login_admin, login_default, fetch_jsonrpc


@pytest.mark.parametrize("test_input, expected", [
    ("password", True),
    ("wrong_pwd", False),
    (" ", False),
    ("", False),
    ("admin", False)
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
    (' ', False),
    ('test.example.com', False),
    ('this is just string', False),
    ("@example.com", False),
    ("email@com", False),
    ("email@.com", False)
])
def test_email_validation(test_input, expected):
    assert email_is_valid(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("+79991234567", True),
    ("79991234567", True),
    ("89991234567", True),
    ("+7(999)123-45-67", True),
    ("8(999)123-45-67", True),
    ('+7123', False),
    ("String again", False)
])
def test_phone_validation(test_input, expected):
    assert phone_is_valid(test_input) == expected


async def test_login(client):
    response = await login_default(client)
    assert response.status == 200

    data = await response.json()
    assert 'result' in data


async def test_login_when_user_does_not_exists(client):
    params = {
        "email": "doesnotexists@example.com",
        "password": "password"
    }
    response = await fetch_jsonrpc(client, "login", params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'User does not exists'


async def test_login_when_password_is_wrong(client):
    params = {
        "email": "testuser@example.com",
        "password": "wrong"
    }
    response = await fetch_jsonrpc(client, "login", params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Password does not match'


async def test_register(client):
    params = {
        "user_name": "new",
        "user_surname": "test",
        "user_email": f"newuser{random.randint(0, 99999999)}@example.com",
        "user_phone": "+79999999999",
        "user_password": "TryGuessQWERTY"
    }

    response = await fetch_jsonrpc(client, "register", params)
    assert response.status == 200

    data = await response.json()
    assert 'result' in data
    assert 'user_id' in data['result']


@pytest.mark.parametrize("email", [
    "wrong.email.com",
    "@example.com",
    "email@",
    "email@com",
    "email@.com",
    " ",
    "",
    "this is just string again"
])
async def test_register_with_invalid_email(client, email):
    params = {
        "user_name": "new",
        "user_surname": "test",
        "user_email": email,
        "user_phone": "+79999999999",
        "user_password": "TryGuessQWERTY"
    }

    response = await fetch_jsonrpc(client, "register", params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Invalid email'


@pytest.mark.parametrize('test_input', [
    '+7123',
    "One more string",
    "",
    " ",
    "123"
])
async def test_register_with_invalid_phone_number(client, test_input):
    params = {
        "user_name": "new",
        "user_surname": "test",
        "user_email": 'invalidphone@example.com',
        "user_phone": test_input,
        "user_password": "TryGuessQWERTY"
    }

    response = await fetch_jsonrpc(client, "register", params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Invalid phone'


async def test_register_when_email_already_exists(client):
    params = {
        "user_name": "new",
        "user_surname": "test",
        "user_email": "testuser@example.com",
        "user_phone": "+79999999999",
        "user_password": "TryGuessQWERTY"
    }

    response = await fetch_jsonrpc(client, "register", params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    # todo: assert error message


@pytest.mark.parametrize('field_name',
                         ['user_name', 'user_surname', 'user_email', 'user_phone', 'user_password'])
async def test_register_with_none_fields(client, field_name):
    params = {"user_name": "new", "user_surname": "test", "user_email": "newuser_withnone@example.com",
              "user_phone": "+79999999993", "user_password": "TryGuessQWERTY", field_name: None}

    response = await fetch_jsonrpc(client, "register", params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data


async def test_login_required_without_login(client):
    # TODO replace with login_required method (not admin_required)
    response = await fetch_jsonrpc(client, "moderating_products_list")
    data = await response.json()
    assert response.status == 200
    assert 'error' in data
    assert data['error']['message'] == 'Auth required'


async def test_login_required(client):
    # todo replace with default login
    await login_admin(client)
    response = await fetch_jsonrpc(client, "moderating_products_list")
    data = await response.json()
    assert response.status == 200
    assert 'result' in data


async def test_view_login_required(client):
    # todo: Implement test
    assert False, "Implement this test"


async def test_admin_required_with_default_user(client):
    await login_default(client)
    response = await fetch_jsonrpc(client, "moderating_products_list")
    data = await response.json()
    assert response.status == 200
    assert 'error' in data
    assert data['error']['message'] == 'Admin required'


async def test_admin_required_without_login(client):
    response = await fetch_jsonrpc(client, "moderating_products_list")
    data = await response.json()
    assert response.status == 200
    assert 'error' in data
    assert data['error']['message'] == 'Auth required'


async def test_admin_required_with_admin(client):
    await login_admin(client)
    response = await fetch_jsonrpc(client, "moderating_products_list")
    data = await response.json()
    assert response.status == 200
    assert 'result' in data


async def test_view_admin_required(client):
    # todo: Implement test
    assert False, "Implement this test"
