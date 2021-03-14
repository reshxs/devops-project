from aiohttp import web
from web.health import health
from web.jrpc_handler import JrpcHandler


def setup_routes(app: web.Application):
    app.router.add_get("/api/health", health, name="health")

    jrpc_handler = JrpcHandler(app)
    app.router.add_get("/api/v1/jsonrpc", jrpc_handler.handle)
