from jsonrpcserver import method
from jsonrpcserver.exceptions import InvalidParamsError

from auth.decorators import login_required
from auth.models import User
from cart.models import Cart, ProductAssignment
from products.models import Product

import sys


@method
@login_required
async def add_to_cart(context, request):
    """
    Example request:
    {
        "jsonrpc": "2.0",
        "method": "add_to_cart",
        "params":
        [
            {
                "product_id": "foo",
                "count": 2
            }
        ]
        "id": "bar"
    }
    """

    # todo: write tests

    objects = context['objects']
    product_id = request.get("product_id", None)
    count = request.get('count', None)

    if not product_id or not count:
        raise InvalidParamsError('product_id or count is None')

    async with objects.atomic():
        user = context['request_obj'].user
        cart = await objects.get_or_create(Cart, user=user)
        product = await objects.get(Product, product_id=product_id)
        # todo: check why generates sync query
        with objects.allow_sync():
            await objects.create(ProductAssignment,
                                 cart=cart[0],
                                 product=product,
                                 count=count)

    return "added"


@method
@login_required
async def remove_from_cart(context, request):
    """
    Example request:
    {
        "jsonrpc": "2.0",
        "method": "remove_from_cart",
        "params":
        [
            {
                "product_id": "foo"
            }
        ]
        "id": "bar"
    }
    """

    # todo: write tests

    objects = context['objects']
    product_id = request.get('product_id', None)
    async with objects.atomic():
        user = context['request_obj'].user
        cart = await objects.get(Cart, user=user)
        product = await objects.get(Product, product_id=product_id)
        # todo: check why generates sync query
        with objects.allow_sync():
            product_assignment = await objects.get(ProductAssignment, cart=cart, product=product)
            await objects.delete(product_assignment)

    return "removed"


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

    objects = context['objects']
    user = context['request_obj'].user
    cart = await objects.get_or_create(Cart, user=user)
    cart = cart[0]
    # todo: check why query is sync
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
