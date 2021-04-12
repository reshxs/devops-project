# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Product(peewee.Model):
    product_id = AutoField(primary_key=True)
    product_name = CharField(max_length=255)
    product_description = TextField()
    product_price = DoubleField()
    product_moderating = BooleanField(default=True)
    product_img_url = CharField(default='', max_length=255)
    class Meta:
        table_name = "product"


@snapshot.append
class User(peewee.Model):
    user_id = AutoField(primary_key=True)
    user_name = CharField(max_length=255)
    user_surname = CharField(max_length=255)
    user_email = CharField(max_length=255, unique=True)
    user_phone = CharField(max_length=255, unique=True)
    user_password = CharField(max_length=255)
    user_is_admin = BooleanField(default=False)
    class Meta:
        table_name = "user"


