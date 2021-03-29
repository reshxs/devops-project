import peewee

from aiohttp_session import get_session
from auth.models import User


async def auth_middleware(app, handler):
    objects = app.objects

    async def middleware(request):
        session = await get_session(request)
        request.user = None
        if 'user_id' in session:
            try:
                request.user = await objects.get(User, user_id=session['user_id'])
            except peewee.DoesNotExist:
                pass

        return await handler(request)

    return middleware
