import aiohttp_jinja2
from jsonrpcserver.exceptions import ApiError
from aiohttp import web

from auth.methods import register
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
        await register(context,
                       user_name=form['user_name'],
                       user_surname=form['user_surname'],
                       user_phone=form['user_phone'],
                       user_email=form['user_email'],
                       user_password=form['user_password'])
        location = request.app.router['login'].url_for()
        raise web.HTTPFound(location)
    except ApiError as e:
        return {'error': str(e)}
