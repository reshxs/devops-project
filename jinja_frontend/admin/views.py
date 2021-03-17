import aiohttp_jinja2

from aiohttp import web
from auth.decorators import view_admin_required
from auth.models import User
from products.models import Product
from peewee import DoesNotExist
from auth.utils import hash_password


@view_admin_required
@aiohttp_jinja2.template('admin/index.html')
async def admin_index(request):
    return {}


@view_admin_required
@aiohttp_jinja2.template('admin/users.html')
async def admin_users(request):
    objects = request.app.objects
    users = await objects.execute(User.select())
    return {'users': users}


@view_admin_required
@aiohttp_jinja2.template('admin/user_details.html')
async def admin_user_details(request):
    objects = request.app.objects
    user_id = request.match_info['id']
    user = await objects.get(User, user_id=user_id)
    return {
        "user": user
    }


@view_admin_required
@aiohttp_jinja2.template('admin/user_edit.html')
async def admin_user_edit(request):
    objects = request.app.objects
    user_id = request.match_info['id']
    user = await objects.get(User, user_id=user_id)
    return {'user': user}


@view_admin_required
@aiohttp_jinja2.template('admin/user_edit.html')
async def admin_user_edit_post(request):
    objects = request.app.objects
    user_id = request.match_info['id']
    user = await objects.get(User, user_id=user_id)
    form = await request.post()

    user.user_email = form['email']
    user.user_name = form['name']
    user.user_surname = form['surname']
    user.user_phone = form['phone']

    is_admin = form.get('is_admin', None)
    user.user_is_admin = True if is_admin else False

    await objects.update(user)

    location = request.app.router['admin_user_details'].url_for(id=user_id)
    raise web.HTTPFound(location)


@view_admin_required
@aiohttp_jinja2.template('admin/user_create.html')
async def admin_user_create(request):
    return {}


@view_admin_required
@aiohttp_jinja2.template('admin.user_create.html')
async def admin_user_create_post(request):
    objects = request.app.objects
    form = await request.post()
    user = await objects.create(User,
                                user_name=form['name'],
                                user_surname=form['surname'],
                                user_email=form['email'],
                                user_phone=form['phone'],
                                user_password=hash_password(form['password']))
    # todo: fix redirect
    location = request.app.router['admin_user_details'].url_for(id=str(user.user_id))
    raise web.HTTPFound(location)


@view_admin_required
@aiohttp_jinja2.template('admin/products.html')
async def admin_products(request):
    objects = request.app.objects
    products = await objects.execute(Product.select())
    return {'products': products}


@view_admin_required
@aiohttp_jinja2.template('admin/product_details.html')
async def admin_product_details(request):
    objects = request.app.objects
    product_id = request.match_info["id"]
    try:
        product = await objects.get(Product, product_id=product_id)
    except DoesNotExist:
        product = None
    return {'product': product}


@view_admin_required
@aiohttp_jinja2.template('admin/product_edit.html')
async def admin_product_edit(request):
    objects = request.app.objects
    product_id = request.match_info['id']
    product = await objects.get(Product, product_id=product_id)
    return {'product': product}


@view_admin_required
@aiohttp_jinja2.template('admin/product_edit.html')
async def admin_product_edit_post(request):
    objects = request.app.objects
    product_id = request.match_info['id']
    product = await objects.get(Product, product_id=product_id)

    form = await request.post()
    product.product_name = form['name']
    product.product_description = form['description']
    product.product_price = float(form['price'])

    on_sale = form.get('on_sale', None)
    product.product_moderating = False if on_sale else True

    await objects.update(product)

    location = request.app.router['admin_product_details'].url_for(id=product_id)
    raise web.HTTPFound(location)
    # return {'product': product}


@view_admin_required
@aiohttp_jinja2.template('admin/product_create.html')
async def admin_product_create(request):
    return {}


@view_admin_required
@aiohttp_jinja2.template('admin/product_create.html')
async def admin_product_create_post(request):
    objects = request.app.objects
    form = await request.post()

    on_sale = form.get('is_moderating')
    product = await objects.create(Product,
                                   product_name=form.get('name'),
                                   product_description=form.get('description'),
                                   product_price=float(form.get('price')),
                                   product_moderating=False if on_sale else True)

    location = request.app.router['admin_products'].url_for()
    raise web.HTTPFound(location)


@view_admin_required
@aiohttp_jinja2.template('admin/user_delete.html')
async def admin_user_delete(request):
    user_id = request.match_info['id']
    objects = request.app.objects
    user = await objects.get(User, user_id=user_id)
    return {'user': user}


@view_admin_required
@aiohttp_jinja2.template('admin/user_delete.html')
async def admin_user_delete_post(request):
    objects = request.app.objects
    form = await request.post()
    user_id = form.get('user_id')
    user = await objects.get(User, user_id=user_id)
    await objects.delete(user)

    location = request.app.router['admin_users'].url_for()
    raise web.HTTPFound(location)


@view_admin_required
@aiohttp_jinja2.template('admin/product_delete.html')
async def admin_product_delete(request):
    product_id = request.match_info['id']
    objects = request.app.objects
    product = await objects.get(Product, product_id=product_id)
    return {'product': product}


@view_admin_required
@aiohttp_jinja2.template('admin/product_delete.html')
async def admin_product_delete_post(request):
    objects = request.app.objects
    form = await request.post()
    product_id = form.get('product_id')
    product = await objects.get(Product, product_id=product_id)
    await objects.delete(product)

    location = request.app.router['admin_products'].url_for()
    raise web.HTTPFound(location)
