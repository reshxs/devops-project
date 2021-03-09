from common.db.models import Product
from server import init_app

import asyncio


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init_app(loop))
    with app.objects.allow_sync():
        Product.drop_table(True)
        Product.create_table(True)
