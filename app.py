from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash 
from flask_login import LoginManager, login_user

import forms
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


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm() # creates instance of form 
    if form.validate_on_submit():  # checks if valid
        flash("Congrats, you're registered!", "success") # second argument is a flash category
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data) # checks to see if user exists
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
        return render_template('login.html', form=form)


@app.route('/')
def index():
    return 'Sup.'   # This is the home page, once logged in


if __name__ == "__main__":
    models.initialize()
    try:

        models.User.create_user(   # created a user for self
            username='n0nb1narydev',
            email='n0nb1narydev@gmail.com',
            password='password1',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)