import asyncio
import logging
import pathlib
import peewee_async
import base64

from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import setup as setup_sessions
from cryptography import fernet
from utils import load_config
from routes import setup_routes
from common.db.db import database
from auth.middleware import auth_middleware

CONF_PATH = pathlib.Path(__file__).parent / 'config.json'


async def init_app(loop: asyncio.AbstractEventLoop):
    conf = load_config(CONF_PATH)
    host, port = conf["host"], conf["port"]

    # Creating an app
    app = web.Application(loop=loop)
    app.jwt_conf = conf['jwt']

    # Setting up sessions
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup_sessions(app, EncryptedCookieStorage(secret_key))


    # Setting up database
    app.database = database
    app.database.init(**conf['database'])
    app.database.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.database, loop=loop)
    app.middlewares.append(auth_middleware)

    # Setting up routes
    setup_routes(app)

    return app, host, port


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init_app(loop))
    web.run_app(app, host=host, port=port)
