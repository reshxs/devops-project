import aio_pika


class ESBClient:
    def __init__(self, connection: aio_pika.Connection):
        self.connection = connection

    async def send_message(self, content: str, routing_key: str = None, exchange_name: str = None) -> None:
        async with self.connection:
            channel = await self.connection.channel()
            if not exchange_name:
                exchange = channel.default_exchange
            else:
                exchange = await channel.declare_exchange(
                    'events', aio_pika.ExchangeType.DIRECT
                )

            await exchange.publish(
                aio_pika.Message(
                    content.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=routing_key
            )
