import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash 
from peewee import *

DATABASE = SqliteDatabase('social.db')


class User(UserMixin, Model): # add to inheritance chain-- Model is the Parent
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length = 100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-join_at',)

    @classmethod
    def create_user(cls, username, email, password, admin=False): # cls is an instance within the method
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_admin=admin
            )
        except IntegrityError: # if not unique
            raise ValueError("User already exists.")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()