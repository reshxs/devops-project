async def fetch_jsonrpc(client, method, params=None):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "id": "test"
    }
    if params:
        data["params"] = params
    result = await client.post('/api/v1/jsonrpc', json=data)
    return result


async def login_admin(client):
    return await fetch_jsonrpc(client, "login", params={"email": "seperuser@example.com", "password": "admin"})


async def login_default(client):
    return await fetch_jsonrpc(client, "login", params={"email": "testuser@example.com", "password": "test"})
