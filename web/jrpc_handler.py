from aiohttp import web
from jsonrpcserver import async_dispatch as dispatch
from web.jrpc_methods import *
import json


class JrpcHandler:
    def __init__(self, app: web.Application):
        self.app = app

    async def handle(self, request: web.Request):
        request_text = await request.text()
        request_json = json.loads(request_text)
        params = request_json.get("params")
        response = await dispatch(request_text, context={'objects': self.app.objects, 'params': params})
        if response.wanted:
            return web.json_response(response.deserialized())
        return web.Response()
