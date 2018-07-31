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

    print(user_name)
    print(password)

    user = User.query.filter(User.user_name == user_name).first()

    user_id = db.session.query(User.user_id).filter(User.user_name == user_name).first()

    if user:
        password_match = db.session.query(User.password).filter(User.user_name == user_name).first()
        password_match = password_match[0]
        if password == password_match:
            session["user_id"]= user_id[0]
            flash("Welcome!")
            return redirect(f"/user_info/{user.user_id}")
        else:
            flash("Login failed. Please double-check your password.")
            return redirect('/login')
    else:
        flash("Looks like you're not registered.  Please register.")
        return redirect('/register')


@app.route('/logout')
def logout():
    """Clears user_id from session"""

    del session['user_id']
    flash("Logged out.")
    return redirect("/login")


@app.route(f"/user_info/<user_id>")
def user_info(user_id):
    """lists students associated with the user"""

    if "user_id" not in session:
        flash("Please log in.")
        return redirect('/login')

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


@app.route("/student_history/<student_id>")
def student_history(student_id):
    """displays student progress-report history"""

    #get student object
    student = Student.query.get(student_id)

    user_id = session["user_id"]

    #get progress object for student (in a list of progress objects).  Loop through these in Jinja and call specific attributes.
    progress = Progress.query.filter(Progress.student_id == student.student_id).all()

    return render_template("student_history.html", student=student, progress=progress, user_id=user_id)


@app.route("/add_progress/<student_id>")
def progress_report(student_id):
    """Gets new progress report info from user"""

    #gets list of all intervention objects from db:
    interventions = db.session.query(Intervention).all()

    #gets list of all behavior objects from db:
    behaviors = db.session.query(Behavior).all()

    #get student object
    student = Student.query.get(student_id)
    user_id = session["user_id"]

    return render_template("progress.html", interventions=interventions, behaviors=behaviors,
                            student_id=student_id, student=student, user_id=user_id,)


@app.route("/add_progress/<student_id>", methods=["POST"])
def add_progress(student_id):
    """adds new progress report to db"""

    interventions = db.session.query(Intervention).all()
    behaviors = db.session.query(Behavior).all()

    date = request.form.get("date")
    behavior_id = request.form.get('behave')
    intervention_id = request.form.get("intervent")
    user_id = session["user_id"]
    rating = request.form.get("rating")
    comment = request.form.get("comment")

    print(behavior_id)
    print(intervention_id)

    #figure out how to make a calendar pop-up on date to select date in datetime.
    #make sure session is connecting to the correct user_id
    progress = Progress(student_id=student_id, date=date, behavior_id=behavior_id,
                        intervention_id=intervention_id, user_id=user_id, rating=rating,
                        comment=comment)

    db.session.add(progress)
    db.session.commit()
    return redirect(f"/student_history/{student_id}")


@app.route("/add_student")
def new_student_form():
    """gets new student info from user"""

    return render_template("new_student.html")


@app.route("/add_student", methods=["POST"])
def add_student():
    """adds a new student to the db"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    user_id = session["user_id"]

    student = Student(fname=fname, lname=lname, user_id=user_id)
    db.session.add(student)
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


@app.route("/interventions")
def display_interventions():
    """displays a list of optional interventions"""

    interventions = db.session.query(Intervention).order_by(Intervention.intervention_name).all()

    return render_template("interventions.html", interventions=interventions)


@app.route("/new_intervention")
def show_intervention_info():
    """gets new intervnetion info from user"""

    return render_template('new_intervention.html')


@app.route("/add_intervention", methods=["POST"])
def add_intervention():
    """adds new intervention to the database"""

    # ideally, I want to only the user that adds this new intervention to see it in the future
    #OR I want to screen to make sure it's appropriate.  Add in functionality.

    intervention_name = request.form.get("intervention_name")
    intervention_description = request.form.get("intervention_description")

    user_id = session["user_id"]

    if len(intervention_description) > 200:
        intervention_description = intervention_description[:200]

    intervention = Intervention(intervention_name=intervention_name, intervention_description=intervention_description)

    db.session.add(intervention)
    db.session.commit()

    return redirect('/interventions')


@app.route("/behaviors")
def display_behaviors():
    """displays a list of optional behaviors"""

    behaviors = db.session.query(Behavior).order_by(Behavior.behavior_name).all()

    return render_template("behaviors.html", behaviors=behaviors)


@app.route("/new_behavior")
def show_behavior_info():
    """gets new behavior info from user"""

    return render_template('new_behavior.html')


@app.route("/add_behavior", methods=["POST"])
def add_behavior():
    """adds new behavior to the database"""

    # ideally, I want to only the user that adds this new behavior to see the new behavior in the future
    #OR I want to screen to make sure it's appropriate.  Add in functionality.

    behavior_name = request.form.get("behavior_name")
    behavior_description = request.form.get("behavior_description")
    user_id = session["user_id"]

    if len(behavior_description) > 200:
        behavior_description = behavior_description[:200]

    behavior = Behavior(behavior_name=behavior_name, behavior_description=behavior_description)

    db.session.add(behavior)
    db.session.commit()

    return redirect('/behaviors')


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