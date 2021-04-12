import pytest

from helpers import fetch_jsonrpc, login_default, login_admin


async def get_cart_when_it_is_empty(client):
    await login_default(client)
    resp = await fetch_jsonrpc(client, 'get_cart')
    assert resp.status == 200

    resp_data = await resp.json()
    assert 'error' in resp_data
    assert resp_data['error']['message'] == 'Cart does not exists'


async def test_get_cart(client):
    await fetch_jsonrpc(client, 'add_to_cart', params={
        "product_id": 1,
        "count": 5
    })

    response = await fetch_jsonrpc(client, 'get_cart')
    assert response.status == 200
    data = await response.json()
    assert 'result' in data
    # todo: test result


async def test_add_to_cart_when_product_does_not_exist(client):
    await login_default(client)
    params = {
        "product_id": -1,
        "count": 1
    }
    resp = await fetch_jsonrpc(client, "add_to_cart", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'error' in data
    assert data['error']['message'] == f"Product {params['product_id']} does not exist"


@pytest.mark.parametrize("count", [
    0, -1, 0.3, 'give_me_a_five'
])
async def test_add_to_cart_with_invalid_count(client, count):
    await login_admin(client)
    params = {
        "product_id": 1,
        "count": count
    }
    resp = await fetch_jsonrpc(client, "add_to_cart", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'error' in data
    assert data['error']['message'] == "Invalid parameters"


async def test_add_to_cart_when_product_already_in_cart(client):
    await login_default(client)
    params = {
        "product_id": 1,
        "count": 2
    }

    await fetch_jsonrpc(client, "add_to_cart", params=params)
    response = await fetch_jsonrpc(client, "add_to_cart", params=params)
    assert response.status == 200

    data = await response.json()
    assert 'result' in data
    assert data['result'] == f"'{params['product_id']}' added to cart"

    response = await fetch_jsonrpc(client, "get_cart")
    data = await response.json()

    assert 'result' in data
    assert str(params['product_id']) in data['result']
    assert data['result'][str(params['product_id'])]['count'] == 4


async def test_add_to_cart(client):
    await login_default(client)
    params = {
        "product_id": 1,
        "count": 2
    }

    response = await fetch_jsonrpc(client, "add_to_cart", params=params)
    assert response.status == 200

    data = await response.json()
    assert 'result' in data
    assert data['result'] == f"'{params['product_id']}' added to cart"


async def test_remove_from_cart_when_product_is_not_in_cart(client):
    await login_default(client)
    await fetch_jsonrpc(client, "add_to_cart", params={
        "product_id": 1,
        "count": 1
    })

    params = {
        "product_id": 2,
    }
    resp = await fetch_jsonrpc(client, "remove_from_cart", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'error' in data
    assert data['error']['message'] == f"Product with id '{params['product_id']}' not in cart"


async def test_remove_from_cart(client):
    await login_default(client)
    await fetch_jsonrpc(client, "add_to_cart", params={
        "product_id": 1,
        "count": 2
    })

    params = {
        "product_id": 1
    }

    response = await fetch_jsonrpc(client, "remove_from_cart", params=params)
    assert response.status == 200

    data = await response.json()
    assert 'result' in data

    response = await fetch_jsonrpc(client, "get_cart")
    data = await response.json()
    assert params["product_id"] not in data


@pytest.mark.parametrize("count", [
    0, -1, 0.3, 'set_fucking_1000'
])
async def test_change_product_count_with_invalid_count(client, count):
    await login_default(client)
    params = {
        "product_id": 1,
        "count": count
    }
    resp = await fetch_jsonrpc(client, "change_product_count", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'error' in data
    assert data['error']['message'] == "Invalid parameters"


async def test_change_product_count_when_product_is_not_in_cart(client):
    await fetch_jsonrpc(client, "add_to_cart", params={
        "product_id": 1,
        "count": 1
    })

    params = {
        "product_id": 2,
        "count": 2
    }
    resp = await fetch_jsonrpc(client, "change_product_count", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'error' in data
    err_msg = f"Product with id '{params['product_id']}' not in cart"
    assert data['error']['message'] == err_msg


async def test_change_product_count(client):
    await login_default(client)
    await fetch_jsonrpc(client, "add_to_cart", params={
        "product_id": 1,
        "count": 1
    })

    params = {
        "product_id": 1,
        "count": 3
    }
    resp = await fetch_jsonrpc(client, "change_product_count", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'result' in data
    assert data['result'] == f"Set count {params['count']} for product {params['product_id']}"
