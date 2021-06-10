# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Product(peewee.Model):
    product_id = PrimaryKeyField(primary_key=True)
    product_name = CharField(max_length=255)
    product_description = TextField()
    product_price = DoubleField()
    product_moderating = BooleanField(default=True)
    product_img_url = CharField(default='', max_length=255)
    class Meta:
        table_name = "product"


@snapshot.append
class User(peewee.Model):
    user_id = PrimaryKeyField(primary_key=True)
    user_name = CharField(max_length=255)
    user_surname = CharField(max_length=255)
    user_email = CharField(max_length=255, unique=True)
    user_phone = CharField(max_length=255, unique=True)
    user_password = CharField(max_length=255)
    user_is_admin = BooleanField(default=False)
    user_registration_confirmed = BooleanField()
    user_registration_code = CharField(max_length=255, null=True)
    class Meta:
        table_name = "user"


def forward(old_orm, new_orm):
    user = new_orm['user']
    return [
        # Apply default value False to the field user.user_registration_confirmed
        user.update({user.user_registration_confirmed: False}).where(user.user_registration_confirmed.is_null(True)),
    ]
