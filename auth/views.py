import aiohttp_jinja2
from jsonrpcserver.exceptions import ApiError
from aiohttp import web

from auth.methods import register
from auth.models import User
from auth.utils import hash_password


@aiohttp_jinja2.template('auth/login.html')
async def login(request):
    # todo: get next url for login or set next url to index
    return {'next_url': '/'}


@aiohttp_jinja2.template('auth/register.html')
async def register(request):
    return {}


@aiohttp_jinja2.template('auth/register.html')
async def register_post(request):
    form = await request.post()
    context = {
        "request_obj": request
    }
    try:
        # todo: fix kwargs error
        user = await register(context,
                              user_name=form['user_name'],
                              user_surname=form['user_surname'],
                              user_phone=form['user_phone'],
                              user_email=form['user_email'],
                              user_password=form['user_password'])
        location = request.app.router['temp-confirm'].url_for() + f'{user.user_id}'
        raise web.HTTPFound(location)
    except ApiError as e:
        return {'error': str(e)}


async def confirm_register(request):
    reg_code = request.match_info.get('uuid')
    objects = request.app['objects']

    user = await objects.get(User, user_registration_code=reg_code)
    user.user_registration_confirmed = True
    user.user_registration_code = None
    await objects.update(user)

    location = request.app.router['shop_index'].url_for()
    raise web.HTTPFound(location)


@aiohttp_jinja2.template('auth/confirm.html')
async def temp_confirm(request):
    user_id = request.match_info.get('id')
    objects = request.app['objects']
    user = await objects.get(User, user_id=user_id)
    location = request.app.router['confirm_register'].url_for(uuid=user.user_registration_code)
    return {
        'location': location
    }
