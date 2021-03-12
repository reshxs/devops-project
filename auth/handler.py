from aiohttp import web
from jsonrpcserver import async_dispatch as dispatch

from auth.methods import *


class AuthHandler:
    # todo implement DRY in handlers
    def __init__(self, app: web.Application):
        self.app = app

    async def handle(self, request: web.Request):
        request_text = await request.text()
        context = {
            'objects': self.app.objects,
            'jwt_conf': self.app.jwt_conf
        }
        response = await dispatch(request_text, context=context)
        if response.wanted:
            return web.json_response(response.deserialized())
        return web.Response()
