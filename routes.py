from aiohttp import web
from web.health import health
from web.jrpc_handler import handle as handle_jrpc


ROUTES = [
    web.get("/api/health", health, name="health"),
    web.get("/api/v1/jsonrpc", handle_jrpc)
]


def setup_routes(app: web.Application):
    app.add_routes(ROUTES)
