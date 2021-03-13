import jwt
from datetime import datetime, timedelta
from jsonrpcserver import method
from jsonrpcserver.exceptions import InvalidParamsError
from auth.models import User
from auth.utils import hash_password, match_password
from peewee import DoesNotExist
from aiohttp_session import get_session


@method
async def login(context, request):
    objects = context['objects']
    jwt_conf = context['jwt_conf']
    request_obj = context['request_obj']
    try:
        user = await objects.get(User, user_email=request.get('email'))
        if match_password(user, request.get('password')):
            payload = {
                'user_id': user.user_id,
                'exp': datetime.utcnow() + timedelta(minutes=jwt_conf['ext_time_delta_min'])
            }
            token = jwt.encode(payload, jwt_conf['secret_key'], jwt_conf['algorithm'])

            session = await get_session(request_obj)
            session['token'] = token
            return {"token": token}
    except DoesNotExist:
        pass

    raise InvalidParamsError("Password doesn't match")


@method
async def register(context, request):
    objects = context['objects']
    user = await objects.create(User,
                                user_name=request.get("user_name"),
                                user_surname=request.get("user_surname"),
                                user_email=request.get("user_email"),
                                user_phone=request.get('user_phone'),
                                user_password=hash_password(request.get("user_password")),
                                user_is_admin=False
                                )
    return {"user_id": user.user_id}
