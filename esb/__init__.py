import aio_pika
import settings


async def send(queue_name: str, message: bytes) -> None:
    conn_string = f"amqp://{settings.RABBIT_LOGIN}:{settings.RABBIT_PASSWORD}@{settings.RABBIT_HOST}/"
    connection = await aio_pika.connect(host=settings.RABBIT_HOST,
                                        port=settings.RABBIT_PORT,
                                        login=settings.RABBIT_LOGIN,
                                        password=settings.RABBIT_PASSWORD)

    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(queue_name)

        await channel.default_exchange.publish(
            aio_pika.Message(message),
            routing_key=queue_name
        )
