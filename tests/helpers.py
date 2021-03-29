import json


async def fetch_jsonrpc(client, method, params=None):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "test"
    }
    if params:
        data["params"] = params
    return await client.post('/api/v1/jsonrpc', data=json.dumps(data))


async def login_admin(client):
    await fetch_jsonrpc(client, "login", params={"email": "seperuser@example.com", "password": "admin"})


async def login_default(client):
    await fetch_jsonrpc(client, "login", params={"email": "testuser@example.com", "password": "test"})