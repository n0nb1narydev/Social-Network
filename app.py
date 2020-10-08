from flask import Flask, g
from flask_login import LoginManager

import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app= Flask(__name__)
app.secret_key = ':/}*vZ+Py-67]tA^ng53gf~XmQ76z]'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # if they aren't logged in, redirect to login


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist: # if user doesn't exist
        return None


@app.before_request
def before_request():
    """Connect to the database."""
    g.db= models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response





if __name__ == "__main__":
    models.initialize()
    models.User.create_user(   # created a user for self
        name='n0nb1narydev',
        email='n0nb1narydev@gmail.com',
        password='password1',
        admin=True
    )
    app.run(debug=DEBUG, host=HOST, port=PORT)