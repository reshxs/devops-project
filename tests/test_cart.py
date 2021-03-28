import json

from helpers import fetch_jsonrpc


async def test_get_cart_with_no_login(client):
    resp = await fetch_jsonrpc(client, 'get_cart')
    assert resp.status == 200

    resp_data = await resp.json()
    assert 'error' in resp_data
    assert resp_data['error']['message'] == 'Auth required'


async def get_cart_when_it_is_empty(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_get_cart(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_add_to_cart_with_no_login(client):
    params = {
        "product_id": 1,
        "count": 1
    }
    resp = await fetch_jsonrpc(client, "add_to_cart", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'error' in data
    assert data['error']['message'] == 'Auth required'


async def test_add_to_cart_with_not_exist_product(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_add_to_cart_with_invalid_count(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_add_to_cart_when_product_already_in_cart(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_add_to_cart(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_remove_from_cart_with_no_login(client):
    params = {
        "product_id": 1,
    }
    resp = await fetch_jsonrpc(client, "remove_from_cart", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'error' in data
    assert data['error']['message'] == 'Auth required'


async def test_remove_from_cart_when_product_is_not_in_cart(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_remove_from_cart(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_change_product_count_with_no_login(client):
    params = {
        "product_id": 1,
        "count": 2
    }
    resp = await fetch_jsonrpc(client, "change_product_count", params=params)

    assert resp.status == 200

    data = await resp.json()
    assert 'error' in data
    assert data['error']['message'] == 'Auth required'


async def test_change_product_count_with_invalid_count(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_change_product_count_when_product_is_not_in_cart(client):
    # todo: implement test
    assert False, "Implement this test"


async def test_change_product_count(client):
    # todo: implement test
    assert False, "Implement this test"
