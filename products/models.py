import peewee
from common.db.models import BaseModel


class Product(BaseModel):
    product_id = peewee.AutoField()
    product_name = peewee.CharField()
    product_description = peewee.TextField()
    product_price = peewee.DoubleField()
    product_moderating = peewee.BooleanField(default=True)
    product_img_url = peewee.CharField(default='')
