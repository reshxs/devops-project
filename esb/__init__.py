import aio_pika
import asyncio
import settings
from aiohttp import web
from .client import ESBClient


def setup(app: web.Application, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()

    esb_client = loop.run_until_complete(get_client())
    app["esb_client"] = esb_client


async def get_client():
    connection = await aio_pika.connect(host=settings.RABBIT_HOST,
                                        port=settings.RABBIT_PORT,
                                        login=settings.RABBIT_LOGIN,
                                        password=settings.RABBIT_PASSWORD)

    return ESBClient(connection)
