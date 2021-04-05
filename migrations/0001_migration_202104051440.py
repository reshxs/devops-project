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



