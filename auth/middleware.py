import jwt
from aiohttp import web
from auth.models import User


async def auth_middleware(app, handler):
    jwt_conf = app.jwt_conf
    objects = app.objects

    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, jwt_conf['secret_key'], algorithms=[jwt_conf['algorithm']])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return web.json_response({"error": "bad token"}, status=400)

            request.user = await objects.get(User, user_id=payload['user_id'])
        return await handler(request)

    return middleware
