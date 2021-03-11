from jsonrpcserver import method
from products.models import Product


@method
async def products_list(context):
    objects = context['objects']
    query = Product.select().where(Product.product_moderating == False)
    products = await objects.execute(query)
    return list(map(lambda g: {
        'good_id': g.product_id,
        'good_name': g.product_name,
        'good_description': g.product_description,
        'good_price': float(g.product_price)
    }, products))


@method
async def moderating_products_list(context):
    objects = context['objects']
    query = Product.select().where(Product.product_moderating == True)
    products = await objects.execute(query)
    return list(map(lambda g: {
        'product_id': g.product_id,
        'product_name': g.product_name,
        'product_description': g.product_description,
        'product_price': g.product_price
    }, products))


@method
async def add_product(context, request):
    objects = context.get('objects')
    inst = await objects.create(Product,
                                product_name=request.get('product_name'),
                                product_description=request.get('product_description'),
                                product_price=request.get('product_price'),
                                product_moderating=request.get('product_moderating'))
    return inst.__dict__['__data__']
