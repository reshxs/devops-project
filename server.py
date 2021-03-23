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

from utils import load_config
from routes import setup_routes
from common.db.db import database
from auth.middleware import auth_middleware

PROJECT_ROOT = pathlib.Path(__file__).parent
CONF_PATH = PROJECT_ROOT / 'config.json'


def init_app():
    conf = load_config(CONF_PATH)
    host, port = conf["host"], conf["port"]

    # Creating an app
    app = web.Application()
    loop = app.loop

    # Setting up sessions
    sessions_conf = conf["sessions"]
    mc_host = os.environ["MEMCACHED_HOST"]
    logging.log(logging.DEBUG, f"connecting to memcached at {mc_host}:{11211}")
    mc = aiomcache.Client(mc_host, 11211, loop=loop)
    setup_sessions(app, MemcachedStorage(mc, max_age=sessions_conf['max_age']))

    # Setting up database
    app.database = database
    db_host = os.environ["DB_HOST"]
    db_port = os.environ["DB_PORT"]
    logging.log(logging.DEBUG, f"connecting to db at {db_host}:{db_port}")
    app.database.init("postgres", host=db_host, port=db_port, user="postgres", password="password")
    app.database.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.database, loop=loop)

    app.middlewares.append(auth_middleware)

    # Setting up jinja
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app['static_root_url'] = 'static'

    # Setting up routes
    setup_routes(app)

    return app, host, port


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    app, host, port = init_app()
    web.run_app(app, host=host, port=port)
    logging.info("Running")
