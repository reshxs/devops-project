from common.db.models import Good
from server import init_app

import asyncio


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init_app(loop))

    with app.objects.allow_sync():
        Good.drop_table(True)
        Good.create_table(True)
