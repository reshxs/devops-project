import asyncio
from common.db.db import database
from auth.models import User
from auth.utils import hash_password
import peewee_async
import typer


"""
Скрипт для создания пользователя с правами администратора
Example: `python3 create_admin.py example@example.com +79999999999 password` 
"""


async def create_user(email: str, phone: str, password: str):
    manager = peewee_async.Manager(database)

    await manager.create(
        User,
        user_email=email,
        user_name='super',
        user_surname='user',
        user_phone=phone,
        user_password=hash_password(password),
        user_is_admin=True
    )

    await manager.close()


def main(email: str, phone: str, password: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_user(
        email=email,
        phone=phone,
        password=password,
    ))
    typer.echo(f"Superuser {email} created")


if __name__ == "__main__":
    typer.run(main)
