import asyncio

import peewee_async
import pytest
import uvloop
from pytest_aiohttp import aiohttp_client
from pytest_aiohttp import TestServer, TestClient

from auth.models import User
from auth.utils import hash_password
from common.db.db import database
from products.models import Product
from server import init_app


# @pytest.fixture(scope="session")
# def loop():
#   loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope='session', autouse=True)
def loop():
    uvloop.install()
    return asyncio.get_event_loop()


async def add_test_data(manager):
    await manager.create_or_get(User,
                                user_name="admin",
                                user_surname="admin",
                                user_email="seperuser@example.com",
                                user_password=hash_password("admin"),
                                user_phone="+79999999999",
                                user_is_admin=True)
    await manager.create_or_get(User,
                                user_name="test",
                                user_surname="user",
                                user_email="testuser@example.com",
                                user_password=hash_password("test"),
                                user_phone="+70000000000",
                                user_is_admin=False)
    await manager.create_or_get(Product,
                                product_id=1,
                                product_name='test',
                                product_description='test',
                                product_price=100,
                                product_moderating=False,
                                product_img_url='example.com/img/1.png')


@pytest.fixture(scope='session')
async def db(loop):
    test_db = database
    test_db.create_tables([User, Product])
    manager = peewee_async.Manager(test_db)

    await add_test_data(manager)

    yield manager
    await manager.close()


@pytest.fixture
async def client(loop, db, aiohttp_client):
    app, host, port = init_app()
    app['objects'] = db
    yield await aiohttp_client(app)
