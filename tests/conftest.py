import asyncio
import pytest
from server import init_app
from pytest_aiohttp import TestServer, TestClient


@pytest.fixture(scope='session')
def loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client(loop):
    app, host, port = init_app()
    server = TestServer(app, loop=loop)
    client = TestClient(server, loop=loop)
    await client.start_server()
    yield client
    await client.close()
