import peewee
from aiohttp_session import get_session
from jsonrpcserver import method
from jsonrpcserver.exceptions import ApiError, InvalidParamsError
from playhouse.shortcuts import model_to_dict, dict_to_model

from auth.decorators import login_required
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

    if not isinstance(count, int) or count <= 0:
        raise InvalidParamsError()

    request = context['request_obj']
    objects = request.app['objects']
    session = await get_session(request)
    cart = {}
    if "cart" in session:
        cart = session["cart"]

    if str(product_id) not in cart:
        try:
            product = await objects.get(Product, product_id=product_id)
        except peewee.DoesNotExist:
            raise ApiError(f"Product {product_id} does not exist")
        cart[product_id] = {
            "product": model_to_dict(product),
            "count": count
            }
    else:
        product_assignment = cart[str(product_id)]
        product_assignment['count'] = int(product_assignment["count"]) + count
        cart[str(product_id)] = product_assignment

    session["cart"] = cart
    return f"'{product_id}' added to cart"


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

    request = context['request_obj']
    session = await get_session(request)

    if 'cart' not in session:
        raise ApiError("Cart does not exist")

    cart = session["cart"]
    if str(product_id) not in cart:
        raise ApiError(f"Product with id '{product_id}' not in cart")

    item = cart.pop(str(product_id))
    product = dict_to_model(Product, item["product"])
    session["cart"] = cart
    return f"{product.product_name}({product.product_id}) removed from cart"


@method
@login_required
async def change_product_count(context, product_id, count):
    """
    Example request:
    {
        "jsonrpc": "2.0",
        "method": "change_product_count",
        "params":
        {
            "product_id": "foo",
            "product_count": 3
        },
        "id": "bar"
    }
    """
    if not isinstance(count, int):
        try:
            count = int(count)
        except ValueError:
            raise InvalidParamsError()

    if count <= 0:
        raise InvalidParamsError()

    request = context["request_obj"]
    session = await get_session(request)
    if 'cart' not in session:
        raise ApiError("Cart does not exist")

    cart = session['cart']
    if str(product_id) not in cart:
        raise ApiError(f"Product with id '{product_id}' not in cart")

    product = cart[str(product_id)]
    product["count"] = count
    cart[str(product_id)] = product
    session["cart"] = cart

    return f"Set count {count} for product {product_id}"


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

    request = context['request_obj']
    session = await get_session(request)
    if 'cart' not in session:
        raise ApiError("Cart does not exists")
    return session['cart']
