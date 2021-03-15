import aiohttp_jinja2
from auth.models import User
from products.models import Product
from aiohttp import web


@aiohttp_jinja2.template('admin/index.html')
async def admin_index(request):
    return {}


@aiohttp_jinja2.template('admin/users.html')
async def admin_users(request):
    objects = request.app.objects
    users = await objects.execute(User.select())
    return {'users': users}


@aiohttp_jinja2.template('admin/user_details.html')
async def admin_user_details(request):
    objects = request.app.objects
    user_id = request.match_info['id']
    user = await objects.get(User, user_id=user_id)
    return {
        "user": user
    }


@aiohttp_jinja2.template('admin/products.html')
async def admin_products(request):
    objects = request.app.objects
    products = await objects.execute(Product.select())
    return {'products': products}


@aiohttp_jinja2.template('admin/product_details.html')
async def admin_product_details(request):
    objects = request.app.objects
    product_id = request.match_info["id"]
    product = await objects.get(Product, product_id=product_id)
    return {'product': product}


@aiohttp_jinja2.template('admin/user_edit.html')
async def admin_user_edit(request):
    objects = request.app.objects
    user_id = request.match_info['id']
    user = await objects.get(User, user_id=user_id)
    return {'user': user}


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

    return {'user': user}


@aiohttp_jinja2.template('admin/product_edit.html')
async def admin_product_edit(request):
    objects = request.app.objects
    product_id = request.match_info['id']
    product = await objects.get(Product, product_id=product_id)
    return {'product': product}


@aiohttp_jinja2.template('admin/product_edit.html')
async def admin_product_edit_post(request):
    objects = request.app.objects
    product_id = request.match_info['id']
    product = await objects.get(Product, product_id=product_id)

    form = await request.post()
    product.product_name = form['name']
    product.product_description = form['description']
    product.product_price = form['price']

    is_moderating = form.get('on_sale', None)
    product.product_moderating = False if is_moderating else True

    await objects.update(product)
    return {'product': product}
