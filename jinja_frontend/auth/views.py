import aiohttp_jinja2


@aiohttp_jinja2.template('auth/login.html')
async def login(request):
    # todo: get next url for login or set next url to index
    return {'next_url': '/'}
