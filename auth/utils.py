import bcrypt
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
