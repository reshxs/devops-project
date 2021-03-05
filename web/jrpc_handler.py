from aiohttp import web
from jsonrpcserver import method, async_dispatch as dispatch


async def handle(request: web.Request):
    request_text = await request.text()
    response = await dispatch(request_text)
    if response.wanted:
        return web.json_response(response.deserialized())
    return web.Response


@method
async def echo(*args):
    return args
