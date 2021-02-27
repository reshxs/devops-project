import asyncio
import logging
import pathlib

from aiohttp import web
from utils import load_config
from routes import setup_routes


PROJ_ROOT = pathlib.Path(__file__).parent


async def init(loop: asyncio.AbstractEventLoop):
    conf = load_config(PROJ_ROOT / 'config.json')
    host, port = conf["host"], conf["port"]

    app = web.Application(loop=loop)
    setup_routes(app)

    return app, host, port


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()
