import jwt
from aiohttp import web
from auth.models import User


async def auth_middleware(app, handler):
    secret = app.jwt_conf['secret_key']
    objects = app.objects

    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                # todo get jst alg from config
                payload = jwt.decode(jwt_token, secret, algorithms=['HS256'])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return web.json_response({"error": "bad token"}, status=400)

            # request.user = User.objects.get(id=payload['user_id'])
            request.user = await objects.get(User, user_id=payload['user_id'])
        return await handler(request)

    return middleware
