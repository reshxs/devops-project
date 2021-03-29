from functools import wraps
from aiohttp import web
from jsonrpcserver.exceptions import ApiError


def login_required(func):
    @wraps(func)
    async def wrapped(context, **kwargs):
        request_obj = context['request_obj']
        if request_obj.user:
            return await func(context, **kwargs)
        raise ApiError("Auth required")

    return wrapped


def admin_required(func):
    @login_required
    @wraps(func)
    async def wrapped(context, **kwargs):
        request_obj = context['request_obj']
        if request_obj.user.user_is_admin:
            return await func(context, **kwargs)
        raise ApiError("Admin required")

    return wrapped


def view_login_required(func):
    @wraps(func)
    async def wrapped(request):
        if request.user:
            return await func(request)

        location = request.app.router['login'].url_for()
        raise web.HTTPFound(location)

    return wrapped


def view_admin_required(func):
    @view_login_required
    @wraps(func)
    async def wrapped(request):
        if request.user.user_is_admin:
            return await func(request)
        return web.Response(text='Admin required')
    return wrapped
