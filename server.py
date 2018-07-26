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
            print(user.user_id)
            flash("Welcome!")
            return redirect(f"/user_info/{user.user_id}")
        else:
            flash("Login failed")
            return redirect('/login')
    else:
        flash("Looks like you're not registered.  Please register.")
        return redirect('/register')


@app.route(f"/user_info/<user_id>")
def user_info(user_id):
    """lists students associated with the user"""

    user = User.query.get(user_id)
    user_name = user.user_name
    user_id = user.user_id

    #This gives you a list of the student objects.  Use SQLAlchemy to reference attributes of each student
    students = user.students

    # user_name = db.session.query(User.user_name).filter(User.user_id == user.user).first()[0]

    # generates list of student names for the user
    student_info = []
    i = 0
    while i < len(students):
        student_info.append((students[i].fname, students[i].lname, students[i].student_id))
        i += 1

    return render_template("user_info.html", user=user, user_name=user_name, user_id=user_id, students=students, student_info=student_info)


@app.route(f"/student_history/<student_id>")
def student_history(student_id):
    """displays student progress-report history"""

    #get student object
    student = Student.query.get(student_id)
    #get student name
    student_name = (student.fname) + " " + (student.lname)
    #get progress object for student (in a list of progress objects).  Loop through these in Jinja and/or call specific attributes.
    progress = db.session.query(Progress).filter(Student.student_id==Progress.student_id).all()


    return render_template("student_history.html", student=student, student_name=student_name, progress=progress)



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
        return redirect('/login')



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