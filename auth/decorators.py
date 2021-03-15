from functools import wraps
from aiohttp import web


def login_required(func):
    @wraps(func)
    async def wrapped(context, request=None):
        request_obj = context['request_obj']
        if request_obj.user:
            if request:
                return await func(context, request)
            return await func(context)
        return {
            "message": "Auth required"
        }

    return wrapped


def admin_required(func):
    @login_required
    @wraps(func)
    async def wrapped(context, request=None):
        request_obj = context['request_obj']
        if request_obj.user.user_is_admin:
            if request:
                return await func(context, request)
            return await func(context)
        return {
            "message": "Admin required"
        }

    return wrapped


def view_login_required(func):
    @wraps(func)
    async def wrapped(request):
        if request.user:
            return await func(request)
        return web.Response(text="Login required")

    return wrapped


def view_admin_required(func):
    @view_login_required
    @wraps(func)
    async def wrapped(request):
        if request.user.user_is_admin:
            return await func(request)
        return web.Response(text='Admin required')
    return wrapped
