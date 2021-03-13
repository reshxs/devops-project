from functools import wraps
from auth.models import User


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
    @wraps(func)
    async def wrapped(context, request=None):
        if context['user_id']:
            user = await context['objects'].get(User, user_id=context['user_id'])
            if user.user_is_admin:
                if request:
                    return await func(context, request)
                return await func(context)
            return {
                "message": "Admin account required!"
            }
        return {
            "message": "Auth required!"
        }

    return wrapped
