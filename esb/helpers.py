import json
from .client import ESBClient
import settings


class EmailClient:
    def __init__(self, client: ESBClient):
        self.client = client

    async def send_message(self, receiver, title, content):
        message = {
            'receiver': receiver,
            'title': title,
            'content': content
        }

        await self.client.send_message(
            json.dumps(message),
            exchange_name=settings.ESB_EMAIL_EXCHANGE,
            routing_key=settings.ESB_EMAIL_ROUTING_KEY
        )
