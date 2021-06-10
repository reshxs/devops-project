from aiohttp import web
from auth.views import *


def setup_auth_routes(app: web.Application):
    app.router.add_get("/auth/login", login, name="login")
    app.router.add_get("/auth/register", register, name='register')
    app.router.add_post("/auth/register", register_post)
    app.router.add_get("/auth/confirm-register/{uuid}", confirm_register, name='confirm_register')
    app.router.add_get("/auth/temp-confirm/{id}", temp_confirm, name='temp_confirm')
