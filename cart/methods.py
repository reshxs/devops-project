import peewee
from jsonrpcserver import method
from jsonrpcserver.exceptions import ApiError

from auth.decorators import login_required
from auth.models import User
from cart.models import Cart, ProductAssignment
from products.models import Product


@method
@login_required
async def add_to_cart(context, product_id, count):
    """
    Example request:
    {
        "jsonrpc": "2.0",
        "method": "add_to_cart",
        "params":
        {
            "product_id": "foo",
            "count": 2
        }
        "id": "bar"
    }
    """

    # todo: write tests

    objects = context['objects']

    if not product_id or not count:
        raise ApiError('product_id or count is None')

    async with objects.atomic():
        user = context['request_obj'].user
        cart = await objects.get_or_create(Cart, user=user)
        try:
            product = await objects.get(Product, product_id=product_id)
        except peewee.DoesNotExist as e:
            raise ApiError(str(e))

        # todo: check why fucking peewee generates sync query
        with objects.allow_sync():
            try:
                await objects.create(ProductAssignment,
                                     cart=cart[0],
                                     product=product,
                                     count=count)
            except peewee.IntegrityError as e:
                raise ApiError(str(e))

    return "added"


@method
@login_required
async def remove_from_cart(context, product_id):
    """
    Example request:
    {
        "jsonrpc": "2.0",
        "method": "remove_from_cart",
        "params":
        {
            "product_id": "foo"
        }
        "id": "bar"
    }
    """

    # todo: write tests

    objects = context['objects']
    async with objects.atomic():
        user = context['request_obj'].user
        try:
            cart = await objects.get(Cart, user=user)
            product = await objects.get(Product, product_id=product_id)

            # todo: check why FUCKING peewee generates sync query
            with objects.allow_sync():
                product_assignment = await objects.get(ProductAssignment, cart=cart, product=product)
                await objects.delete(product_assignment)

        except peewee.DoesNotExist as e:
            raise ApiError(str(e))

    return f"removed {product_assignment.product.product_id}"


@method
@login_required
async def get_cart(context):
    """
    Example request:
    {
        "jsonrpc": "2.0",
        "method": "get_cart",
        "id": "foo"
    }
    """
    # todo: writer tests

    objects = context['request_obj'].app.objects
    user = context['request_obj'].user
    cart = await objects.get_or_create(Cart, user=user)
    cart = cart[0]
    # todo: check why FUCKING query is sync
    with objects.allow_sync():
        product_assignments = await objects.execute(ProductAssignment.select().where(ProductAssignment.cart == cart))

        result = list()

        # todo: check why related object call is sync
        for product in map(lambda pa: pa.product, product_assignments):
            result.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'product_price': product.product_price
            })

    return result
