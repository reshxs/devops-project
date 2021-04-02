from aiohttp import web
from auth.views import *


def setup_auth_routes(app: web.Application):
    app.router.add_get("/auth/login", login, name="login")
