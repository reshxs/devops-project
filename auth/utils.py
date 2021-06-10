import re

import bcrypt
import settings

from auth.models import User
from esb.helpers import EmailClient


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode("utf-8")


def match_password(user: User, password: str) -> bool:
    password = password.encode("utf-8")
    user_password = user.user_password.encode("utf-8")
    return bcrypt.checkpw(password, user_password)


def email_is_valid(email):
    return bool(re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', email))


def phone_is_valid(phone):
    return bool(re.search('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone))


def password_is_valid(password: str):
    return len(password) >= 6 and re.search('[A-Z]+[a-z]+\w{1,}', password)


async def send_email_confirmation(client: EmailClient, user: User) -> None:
    if user.user_registration_confirmed:
        return

    confirmation_link = f'{settings.BASE_URL}/auth/confirm_registration/{user.user_registration_code}'

    await client.send_message(
        receiver=user.user_email,
        title="Подтверждение регистрации",
        content=f"Подтверждить регистрацию: {confirmation_link}"
    )
