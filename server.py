from flask import (Flask, render_template, redirect, request, flash, session)

from datetime import datetime

from model import User, Student, Behavior, Intervention, Progress, app

import random

from jinja2 import StrictUndefined

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

app = Flask(__name__)

app.secret_key = "behavior"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")


@app.route('/login')
def user_login():
    """gets username and password from user"""

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def check_login():
    """login existing users"""

    user_name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter(User.user_name == user_name).first()

    password_match = db.session.query(User.password).filter(User.user_name == user_name).first()[0]

    user_id = db.session.query(User.user_id).filter(User.user_name == user_name).first()

    if user:
        if password == password_match:
            session["user_id"] = user_id
            flash("Welcome!")
            return redirect('/user_info')
        else:
            flash("Login failed")
            return redirect('/login')
    else:
        flash("Looks like you're not registered.  Please register.")
        return redirect('/register')

    # name_match = User.query.filter(User.user_name == user_name, User.password == password).first()
    # # password = User.query.filter(User.password == password).first()

    # if name_match:
    #     # if password:
    #         session["user_name"] = User.user_id
    #         flash("Welcome!  You're logged in.")
    #         return render_template("/user_info.html")
    # else:
    #     flash("There was a problem with your username or password.  Please login or register.")
    #     return redirect("/login")


@app.route('/user_info')
def user_info():
    """lists students associated with the user"""

    return render_template("user_info.html")


@app.route('/register')
def user_register():
    """Gets email and password from user"""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_new_user():
    """adds new user to the db"""

    user_name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter(User.user_name == user_name).first()

    if user:
        flash("That user_name is already registered.  Please choose another name.")
        return redirect('/register')
    else:
        user_name = User(user_name=user_name, password=password)
        db.session.add(user_name)
        db.session.commit()
        return redirect('/user_info')


if __name__ == "__main__":
    # Set debug=True, it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    #DebugToolbar 
    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")