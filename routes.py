from aiohttp import web
import pathlib
from web.health import health
from web.jrpc_handler import JrpcHandler
from admin.routes import setup_admin_routes
from auth.routes import setup_auth_routes
from shop.routes import setup_shop_routes

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app: web.Application):
    app.router.add_get("/api/health", health, name="health")

    jrpc_handler = JrpcHandler(app)
    app.router.add_post("/api/v1/jsonrpc", jrpc_handler.handle)

    setup_admin_routes(app)
    setup_auth_routes(app)
    setup_shop_routes(app)

    app.router.add_static('/static/', path=PROJECT_ROOT / 'frontend' / 'static', name="static")
