from aiohttp import web
from jsonrpcserver import async_dispatch as dispatch
from auth.decorators import login_required

from web.jrpc_methods import *
from products.methods import *
from cart.methods import *


class JrpcHandler:
    def __init__(self, app: web.Application):
        self.app = app

    async def handle(self, request: web.Request):
        request_text = await request.text()
        context = {
            'objects': self.app.objects,
            'user_id': request.user
        }
        response = await dispatch(request_text, context=context)
        if response.wanted:
            return web.json_response(response.deserialized())
        return web.Response()
