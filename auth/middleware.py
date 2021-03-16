from aiohttp_session import get_session
from auth.models import User


async def auth_middleware(app, handler):
    objects = app.objects

    async def middleware(request):
        session = await get_session(request)
        request.user = None
        # todo: check uid from session
        if 'user_id' in session:
            request.user = await objects.get(User, user_id=session['user_id'])

        return await handler(request)

    return middleware
