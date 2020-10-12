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
        order_by = ('-join_at',) # tuple... must have comma even if 1 item

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):   # our posts, plus the posts of the users we follow
        return Post.select().where(
            (Post.user << self.following()) |   # << is the equivalent to the 'in' keyword --   | <= means 'or'
            (Post.user == self),
            # add posts from other users here
        )


    @classmethod
    def create_user(cls, username, email, password, admin=False): # cls is an instance within the method
        try:
            with models.DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError: # if not unique
            raise ValueError("User already exists.")

    def following(self):
        """ The users that we are following. """
        return (
            User.select().join(   
                Relationship, on=Relationship.to_user # Select all users where the from_user is "me"
            ).where(
                Relationsip.from_user == self   
            )
        )

    def followers(self):
        """ The users that are following current user """
        return user.select().join(
            Relationship, on=Relationship.from_user
        ).where(
            Relationship.to_user == self
        )




class Post(Model):  # not a user... so UserMixin not needed
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField( 
        rel_model=User, # Foreign key points to User Model
        related_name='posts' # what you call this
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',) # newest posts first -- tuple... must have comma even if 1 item


class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = databaseindexes = (
            (('from_user', 'to_user'),True)
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Relationship], safe=True)
    DATABASE.close()