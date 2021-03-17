from datetime import datetime, timedelta

import aiohttp_jinja2
from auth.models import User
from auth.utils import match_password


@aiohttp_jinja2.template('auth/login.html')
async def login(request):
    return {'next_url': '/'}
