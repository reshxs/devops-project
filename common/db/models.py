import peewee

from common.db.db import database


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Good(BaseModel):
    good_id = peewee.CharField(unique=True, null=False)
    good_name = peewee.CharField()
    good_description = peewee.TextField()
    good_price = peewee.DecimalField()
    good_moderating = peewee.BooleanField(default=True)
