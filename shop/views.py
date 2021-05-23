import aiohttp_jinja2
from peewee import DoesNotExist

from products.models import Product


@aiohttp_jinja2.template("shop/index.html")
async def index(request):
    return {'user': request.user}


@aiohttp_jinja2.template("shop/catalog.html")
async def catalog(request):
    return {'user': request.user}


@aiohttp_jinja2.template("shop/cart.html")
async def cart(request):
    return {'user': request.user}


@aiohttp_jinja2.template("shop/profile.html")
async def profile(request):
    return {'user': request.user}


@aiohttp_jinja2.template("shop/support.html")
async def support(request):
    return {'user': request.user}


@aiohttp_jinja2.template("shop/product_details.html")
async def product_details(request):
    objects = request.app['objects']
    product_id = request.match_info["id"]
    try:
        product = await objects.get(Product, product_id=product_id)
    except DoesNotExist:
        product = None
    return {'user': request.user, 'product': product}
