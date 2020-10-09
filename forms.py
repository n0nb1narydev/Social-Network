from flask_wtf import Form 
from wtforms import (StringField, PasswordField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists(): # returns a boolean
        raise ValueError('Username is already in use.')

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValueError('Email is already in use.')


class RegisterForm(Form):
    username = StringField(
        'Username',    # first argument is the label
        validators=[
            DataRequired(), # field cannot be empty
            Regexp(         #regular expression pattern
                r'^[a-zA-Z-0-9_]+$', # askie  Unicode is also an option
                message=("Username should be one word, letters, " 
                        "numbers, and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(), # cannot be blank
            Email(), # must be an email
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match.') # verifies the password by making them type the password twice
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])