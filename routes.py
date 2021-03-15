from aiohttp import web
import pathlib
from web.health import health
from web.jrpc_handler import JrpcHandler
from jinja_frontend.admin.views import *
from jinja_frontend.auth.views import *

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app: web.Application):
    app.router.add_get("/api/health", health, name="health")

    jrpc_handler = JrpcHandler(app)
    app.router.add_post("/api/v1/jsonrpc", jrpc_handler.handle)

    app.router.add_get("/admin", admin_index, name="admin_index")
    app.router.add_get("/admin/users", admin_users, name='admin_users')
    app.router.add_get("/admin/products", admin_products, name="admin_products")
    app.router.add_get("/admin/users/{id}", admin_user_details, name="admin_user_details")
    app.router.add_get("/admin/products/{id}", admin_product_details, name="admin_product_details")
    app.router.add_get("/admin/users/{id}/edit", admin_user_edit, name="admin_user_edit")
    app.router.add_post("/admin/users/{id}/edit", admin_user_edit_post)
    app.router.add_get("/admin/products/{id}/edit", admin_product_edit, name="admin_product_edit")
    app.router.add_post("/admin/products/{id}/edit", admin_product_edit_post)
    app.router.add_get("/auth/login", login, name="login")

    app.router.add_static('/static/', path=PROJECT_ROOT / 'static', name="static")


