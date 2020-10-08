from flask_wtf import Form 
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, ValidationError

from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists() # returns a boolean
        raise ValueError('Username is already in use.')


class RegisterForm(Form):
    username = StringField(
        'Username',    # first argument is the label
        validators-[
            DataRequired(), # field cannot be empty
            Regexp(         #regular expression pattern
                r'^[a-zA-Z-0-9_]+$', # askie  Unicode is also an option
                message=("Username should be one word, letters, " 
                        "numbers, and underscores only.")
            ),
            name_exists()
        ])
    email = StringField(
        'Email',
        validators-[
            DataRequired(),
            Regexp(
                
            )
        ]
    )