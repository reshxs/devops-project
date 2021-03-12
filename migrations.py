from products.models import Product
from auth.models import User
from cart.models import ProductAssignment, Cart
from server import init_app

import asyncio


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init_app(loop))
    with app.objects.allow_sync():
        Product.create_table(True)
        User.create_table(True)
        Cart.create_table(True)
        ProductAssignment.create_table(True)
