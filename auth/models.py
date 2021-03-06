import peewee
from common.db.models import BaseModel


class User(BaseModel):
    user_id = peewee.AutoField()
    user_name = peewee.CharField(null=False)
    user_surname = peewee.CharField(null=False)
    user_email = peewee.CharField(null=False, unique=True)
    user_phone = peewee.CharField(null=False)
    user_password = peewee.CharField(null=False)
    user_is_admin = peewee.BooleanField(default=False)
