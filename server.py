import asyncio
import logging
import pathlib
import peewee_async
import jinja2
import aiohttp_jinja2
import os

from aiohttp import web
import aiomcache
from aiohttp_session.memcached_storage import MemcachedStorage
from aiohttp_session import setup as setup_sessions

from auth.models import User
from cart.models import Cart, ProductAssignment
from products.models import Product
from utils import load_config
from routes import setup_routes
from common.db.db import database
from auth.middleware import auth_middleware

PROJECT_ROOT = pathlib.Path(__file__).parent
CONF_PATH = PROJECT_ROOT / 'config.json'


async def init_app(loop: asyncio.AbstractEventLoop):
    conf = load_config(CONF_PATH)
    host, port = conf["host"], conf["port"]

    # Creating an app
    app = web.Application(loop=loop)

    # Setting up sessions
    sessions_conf = conf["sessions"]
    mc_host = os.environ["MEMCACHED_HOST"]
    mc = aiomcache.Client(mc_host, 11211, loop=loop)
    setup_sessions(app, MemcachedStorage(mc, max_age=sessions_conf['max_age']))

    # Setting up database
    app.database = database
    db_host = os.environ["DB_HOST"]
    app.database.init("postgres", host=db_host, user="postgres", password="password")
    app.database.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.database, loop=loop)

    # TODO: REMOVE THIS SHIT
    with app.objects.allow_sync():
        Product.create_table(True)
        User.create_table(True)
        Cart.create_table(True)
        ProductAssignment.create_table(True)

    app.middlewares.append(auth_middleware)

    # Setting up jinja
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app['static_root_url'] = 'static'

    # Setting up routes
    setup_routes(app)

    return app, host, port


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init_app(loop))
    web.run_app(app, host=host, port=port)
