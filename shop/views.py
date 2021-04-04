import aiohttp_jinja2
from products.models import Product


@aiohttp_jinja2.template("shop/index.html")
async def index(request):
    return {'user': request.user}


@aiohttp_jinja2.template("shop/catalog.html")
async def catalog(request):
    return {'user': request.user}