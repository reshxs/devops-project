import bcrypt
import re
from auth.models import User


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
