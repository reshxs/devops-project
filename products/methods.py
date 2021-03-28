import peewee
from jsonrpcserver import method
from jsonrpcserver.exceptions import ApiError

from products.models import Product
from auth.decorators import login_required, admin_required


@method
async def products_list(context):
    objects = context['objects']
    query = Product.select().where(Product.product_moderating == False)
    products = await objects.execute(query)
    return list(map(lambda g: {
        'product_id': g.product_id,
        'product_name': g.product_name,
        'product_description': g.product_description,
        'product_price': float(g.product_price)
    }, products))


@method
@admin_required
async def moderating_products_list(context):
    objects = context['objects']
    query = Product.select().where(Product.product_moderating == True)
    products = await objects.execute(query)
    return list(map(lambda g: {
        'product_id': g.product,
        'product_name': g.product_name,
        'product_description': g.product_description,
        'product_price': g.product_price
    }, products))


@method
@admin_required
async def add_product(context, product_name, product_description, product_price, product_moderating):
    objects = context.get('objects')
    try:
        inst = await objects.create(Product,
                                    product_name=product_name,
                                    product_description=product_description,
                                    product_price=product_price,
                                    product_moderating=product_moderating)
    except peewee.IntegrityError as e:
        raise ApiError(str(e))
    return inst.__dict__['__data__']
