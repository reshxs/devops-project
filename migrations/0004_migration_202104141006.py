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
    user_firstname = CharField(max_length=255)
    user_lastname = CharField(max_length=255)
    user_email = CharField(max_length=255, unique=True)
    user_phone = CharField(max_length=255, unique=True)
    user_password = CharField(max_length=255)
    user_is_admin = BooleanField(default=False)
    class Meta:
        table_name = "user"


def forward(old_orm, new_orm):
    user = new_orm['user']
    return [
        # Apply default value '' to the field user.user_lastname
        user.update({user.user_lastname: ''}).where(user.user_lastname.is_null(True)),
        # Apply default value '' to the field user.user_firstname
        user.update({user.user_firstname: ''}).where(user.user_firstname.is_null(True)),
    ]


def backward(old_orm, new_orm):
    user = new_orm['user']
    return [
        # Apply default value '' to the field user.user_name
        user.update({user.user_name: ''}).where(user.user_name.is_null(True)),
        # Apply default value '' to the field user.user_surname
        user.update({user.user_surname: ''}).where(user.user_surname.is_null(True)),
    ]
