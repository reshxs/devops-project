from aiohttp import web
from web.health import health
from web.jrpc_handler import JrpcHandler


def setup_routes(app: web.Application):
    app.router.add_get("/api/health", health, name="health")

    handler = JrpcHandler(app)
    app.router.add_get("/api/v1/jsonrpc", handler.handle)
