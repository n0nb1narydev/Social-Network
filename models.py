import datetime

from peewee import *

DATABASE = SqliteDatabase('social.db')


class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = Charfield(max_length = 100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-join_at',)

