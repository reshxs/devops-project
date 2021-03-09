import peewee

from common.db.db import database


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Product(BaseModel):
    product_id = peewee.AutoField()  # (unique=True, null=False, primary_key=True)
    product_name = peewee.CharField()
    product_description = peewee.TextField()
    product_price = peewee.DoubleField()
    product_moderating = peewee.BooleanField(default=True)
