from aiohttp import web
from .views import *


def setup_shop_routes(app: web.Application):
    app.router.add_get("/", index, name="shop_index")
    app.router.add_get("/catalog", catalog, name="shop_catalog")
    app.router.add_get("/cart", cart, name="shop_cart")
    app.router.add_get("/profile", profile, name="shop_profile")
    app.router.add_get("/support", support, name="shop_support")
