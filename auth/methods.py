import peewee

from jsonrpcserver import method
from jsonrpcserver.exceptions import InvalidParamsError, ApiError
from auth.models import User
from auth.utils import hash_password, match_password, email_is_valid
from auth.decorators import login_required
from aiohttp_session import get_session


@method
async def login(context, email, password):
    objects = context['request_obj'].app['objects']
    request_obj = context['request_obj']
    try:
        user = await objects.get(User, user_email=email)
        if match_password(user, password):
            session = await get_session(request_obj)
            session['user_id'] = user.user_id
            return {
                "status": "ok"
            }
    except peewee.DoesNotExist:
        raise ApiError("User does not exists")

    raise ApiError("Password does not match")


@method
@login_required
async def logout(context):
    request_obj = context['request_obj']
    session = await get_session(request_obj)
    session["user_id"] = None
    return {
        "message": "logged out"
    }


@method
async def register(context, user_name, user_surname, user_email, user_phone, user_password):
    if not email_is_valid(user_email):
        raise ApiError("Invalid email")

    objects = context['request_obj'].app['objects']
    try:
        user = await objects.create(User,
                                    user_name=user_name,
                                    user_surname=user_surname,
                                    user_email=user_email,
                                    user_phone=user_phone,
                                    user_password=hash_password(user_password),
                                    user_is_admin=False
                                    )
    except peewee.IntegrityError as error:
        raise ApiError(str(error))

    return {"user_id": user.user_id}
