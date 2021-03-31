from aiohttp import web
import pathlib
from web.health import health
from web.jrpc_handler import JrpcHandler
from frontend.auth.views import *
from frontend.admin.routes import setup_admin_routes

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app: web.Application):
    app.router.add_get("/api/health", health, name="health")

    jrpc_handler = JrpcHandler(app)
    app.router.add_post("/api/v1/jsonrpc", jrpc_handler.handle)

    setup_admin_routes(app)
    app.router.add_get("/auth/login", login, name="login")

    app.router.add_static('/static/', path=PROJECT_ROOT / 'frontend' / 'static', name="static")


