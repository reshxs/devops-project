import peewee
from common.db.models import BaseModel
from auth.models import User
from products.models import Product


class Cart(BaseModel):
    user = peewee.ForeignKeyField(User, backref='cart', unique=True, primary_key=True)


class ProductAssignment(BaseModel):
    cart = peewee.ForeignKeyField(Cart, backref='product_assignments')
    product = peewee.ForeignKeyField(Product, backref='product_assignment')
    count = peewee.IntegerField()
