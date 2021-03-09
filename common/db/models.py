import peewee

from common.db.db import database


class BaseModel(peewee.Model):
    class Meta:
        database = database
