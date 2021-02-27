from aiohttp import web
from web.health import health
from web.jrpc_handler import handle as handle_jrpc


def setup_routes(app: web.Application):
    router = app.router
    router.add_get("/api/health", health, name="health")
    router.add_get("/api/v1/jsonrpc", handle_jrpc)
