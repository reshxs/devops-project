import pytest

from helpers import fetch_jsonrpc, login_admin


async def test_products_list(client):
    response = await fetch_jsonrpc(client, 'products_list')
    assert response.status == 200

    data = await response.json()
    assert 'result' in data


async def test_moderating_products_list_with_no_login(client):
    response = await fetch_jsonrpc(client, "moderating_products_list")
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Auth required'


async def test_moderating_products_list_with_no_admin(client):
    await fetch_jsonrpc(client, "login", params={"email": "testuser@example.com", "password": "test"})
    response = await fetch_jsonrpc(client, "moderating_products_list")
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Admin required'


async def test_moderating_products_list(client):
    await login_admin(client)
    response = await fetch_jsonrpc(client, "moderating_products_list")
    assert response.status == 200

    data = await response.json()
    assert 'result' in data


async def test_add_product_with_no_login(client):
    params = {
        "product_name": "new_product",
        "product_description": "test",
        "product_price": 99.99,
        "product_moderating": True
    }
    response = await fetch_jsonrpc(client, "add_product", params=params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Auth required'


async def test_add_product_with_no_admin(client):
    await fetch_jsonrpc(client, "login", params={"email": "testuser@example.com", "password": "test"})
    params = {
        "product_name": "new_product",
        "product_description": "test",
        "product_price": 99.99,
        "product_moderating": True
    }
    response = await fetch_jsonrpc(client, 'add_product', params=params)
    assert response.status == 200

    data = await response.json()

    assert 'error' in data
    assert data['error']['message'] == 'Admin required'


# todo: add more invalid values
@pytest.mark.parametrize("name, description, price", [
    ('new', 'desc', 'string')
])
async def test_add_product_with_invalid_parameters(client, name, description, price):
    await login_admin(client)
    params = {
        "product_name": name,
        "product_description": description,
        "product_price": price,
        "product_moderating": False
    }
    response = await fetch_jsonrpc(client, 'add_product', params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Invalid parameters'


@pytest.mark.parametrize("name, description, price", [
    ('new', 'desc', 1),
    ('new', 'desc', 1.9),
])
async def test_add_product_and_remove_product(client, name, description, price):
    await login_admin(client)
    params = {
        "product_name": name,
        "product_description": description,
        "product_price": price,
        "product_moderating": False
    }
    response = await fetch_jsonrpc(client, 'add_product', params)
    assert response.status == 200

    data = await response.json()
    assert 'result' in data
    assert data['result']['product_name'] == name
    assert data['result']['product_description'] == description
    assert data['result']['product_price'] == price
    assert not data['result']['product_moderating']

    # Try to remove product and assert that product removed
    p_id = data['result']['product_id']
    response = await fetch_jsonrpc(client, 'delete_product', params={'product_id': p_id})
    data = await response.json()
    assert data['result'] == f"Removed product {p_id}"


async def test_remove_product_when_product_does_not_exits(client):
    await login_admin(client)
    params = {
        "product_id": -1
    }

    response = await fetch_jsonrpc(client, 'delete_product', params=params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Product -1 does not exist'


async def test_remove_product_with_invalid_product_id(client):
    await login_admin(client)
    params = {
        "product_id": 'str'
    }

    response = await fetch_jsonrpc(client, 'delete_product', params=params)
    assert response.status == 200

    data = await response.json()
    assert 'error' in data
    assert data['error']['message'] == 'Invalid parameters'
