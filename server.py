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