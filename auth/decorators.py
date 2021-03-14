from functools import wraps


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
