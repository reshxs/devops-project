import peewee
from jsonrpcserver import method
from jsonrpcserver.exceptions import ApiError, InvalidParamsError

from products.models import Product
from auth.decorators import login_required, admin_required


@method
async def products_list(context):
    objects = context['request_obj'].app['objects']
    query = Product.select().where(Product.product_moderating == False)
    products = await objects.execute(query)
    return list(map(lambda p: {
        'product_id': p.product_id,
        'product_name': p.product_name,
        'product_description': p.product_description,
        'product_price': float(p.product_price)
    }, products))


@method
@admin_required
async def moderating_products_list(context):
    objects = context['request_obj'].app['objects']
    query = Product.select().where(Product.product_moderating == True)
    products = await objects.execute(query)
    return list(map(lambda p: {
        'product_id': p.product_id,
        'product_name': p.product_name,
        'product_description': p.product_description,
        'product_price': p.product_price
    }, products))


@method
@admin_required
async def add_product(context, product_name, product_description, product_price, product_moderating):
    objects = context['request_obj'].app['objects']
    try:
        inst = await objects.create(Product,
                                    product_name=product_name,
                                    product_description=product_description,
                                    product_price=product_price,
                                    product_moderating=product_moderating)
    except peewee.IntegrityError as e:
        raise ApiError(str(e))
    except peewee.DataError:
        raise InvalidParamsError
    return inst.__dict__['__data__']


@method
@admin_required
async def delete_product(context, product_id):
    objects = context['request_obj'].app['objects']
    try:
        product = await objects.get(Product, product_id=product_id)
        await objects.delete(product)
    except peewee.DoesNotExist:
        raise ApiError(f'Product {product_id} does not exist')
    except peewee.DataError:
        raise InvalidParamsError()

    return f"Removed product {product_id}"
