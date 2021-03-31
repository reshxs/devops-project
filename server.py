import logging

import aiohttp_jinja2
import aiomcache
import jinja2
import peewee_async
from aiohttp import web
from aiohttp_session import setup as setup_sessions
from aiohttp_session.memcached_storage import MemcachedStorage

import settings
from auth.middleware import auth_middleware
from common.db.db import database
from routes import setup_routes


def init_app():
    logging.log(logging.DEBUG, f"App: {settings.HOST=}, {settings.PORT=}")

    # Creating an app
    app = web.Application()

    # Setting up sessions
    logging.log(logging.DEBUG, f"Memcached: {settings.MEMCACHED_HOST=}, {settings.MEMCACHED_PORT=}")
    mc = aiomcache.Client(settings.MEMCACHED_HOST, settings.MEMCACHED_PORT)
    setup_sessions(app, MemcachedStorage(mc, max_age=settings.SESSION_MAX_AGE))

    # Setting up database
    logging.log(logging.DEBUG, f"DB: {settings.DB_HOST=}, {settings.DB_PORT=}")
    app.database = database
    app.database.init("postgres",
                      host=settings.DB_HOST,
                      port=settings.DB_PORT,
                      user=settings.DB_USER,
                      password=settings.DB_PASSWORD)

    app.database.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.database)

    app.middlewares.append(auth_middleware)

    # Setting up jinja
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('frontend/templates'))
    app['static_root_url'] = 'frontend/static'

    # Setting up routes
    setup_routes(app)
    logging.log(logging.DEBUG, "Running...")

    return app, settings.HOST, settings.PORT


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    app, host, port = init_app()
    web.run_app(app, host=host, port=port)
    logging.info("Running")
