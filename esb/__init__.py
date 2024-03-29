import logging

import aio_pika
import asyncio
import settings
from aiohttp import web
from .client import ESBClient


async def on_shutdown(app):
    await app["esb_client"].close()


def setup(app: web.Application, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()

    esb_client = loop.run_until_complete(get_client())
    app["esb_client"] = esb_client
    app.on_shutdown.append(on_shutdown)


async def get_client():
    for i in range(30):
        try:
            connection = await aio_pika.connect(host=settings.RABBIT_HOST,
                                                port=settings.RABBIT_PORT,
                                                login=settings.RABBIT_LOGIN,
                                                password=settings.RABBIT_PASSWORD)
        except ConnectionError as e:
            if i == 29:
                raise
            logging.log(logging.INFO, str(e))
            await asyncio.sleep(1)
        else:
            return ESBClient(connection)
