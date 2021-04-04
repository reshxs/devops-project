from aiohttp import web
from .views import *


def setup_shop_routes(app: web.Application):
    app.router.add_get("/", index, name="shop_index")
    app.router.add_get("/catalog", catalog, name="shop_catalog")
