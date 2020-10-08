import datetime

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from peewee import *

DATABASE = SqliteDatabase('social.db')


class User(UserMixin, Model): # add to inheritance chain-- Model is the Parent
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = Charfield(max_length = 100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-join_at',)

    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_admin=admin
            )

