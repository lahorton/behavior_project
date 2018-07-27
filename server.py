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

    return render_template("user_info.html", user=user, user_name=user_name,
                            user_id=user_id, students=students,
                            student_info=student_info)


@app.route(f"/student_history/<student_id>")
def student_history(student_id):
    """displays student progress-report history"""

    #get student object
    student = Student.query.get(student_id)
    #get student name
    student_name = (student.fname) + " " + (student.lname)

    #get progress object for student (in a list of progress objects).  Loop through these in Jinja and/or call specific attributes.
    progress = db.session.query(Progress).filter(Student.student_id==Progress.student_id).order_by(Progress.date.desc()).all()
    intervention_name = db.session.query(Intervention.intervention_name).filter(Progress.intervention_id==Intervention.intervention_id).first()[0]
    behavior_name = db.session.query(Behavior.behavior_name).filter(Progress.behavior_id==Behavior.behavior_id).first()[0]

    return render_template("student_history.html", student=student,
                            student_name=student_name, progress=progress,
                            behavior_name=behavior_name, intervention_name=intervention_name)


@app.route("/add_progress/")
def progress_report():
    """Gets new progress report info from user"""

    #gets list of all intervention objects from db:
    interventions = db.session.query(Intervention).all()

    #gets list of all behavior objects from db:
    behaviors = db.session.query(Behavior).all()

    return render_template("progress.html", interventions=interventions, behaviors=behaviors)


@app.route("/add_progress", methods=["POST"])
def add_progress():
    """adds new progress report to db"""

    interventions = db.session.query(Intervention).all()
    behaviors = db.session.query(Behavior).all()

    student_id = request.form.get("student_id")
    date = request.form.get("date")
    behavior_id = request.form.get("behavior.behavior_id")
    intervention_id = request.form.get("intervention.intervention_id")
    user_id = session["user_id"][0]
    rating = request.form.get("rating")
    comment = request.form.get("comment")


    #figure out how to make a calendar pop-up on date to select date in datetime.
    #make sure session is connecting to the correct user_id

    progress = Progress(student_id=student_id, date=date, behavior_id=behavior.behavior_id,
                        intervention_id=intervention.intervention_id, user_id=user_id, rating=rating,
                        comment=comment)

    db.session.add(progress)
    db.session.commit()
    return redirect(f"/user_info/{user_id}")


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