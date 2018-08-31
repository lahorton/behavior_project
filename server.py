from flask import (Flask, render_template, redirect, request, flash, session)
from datetime import datetime
from model import User, Student, Behavior, Intervention, Progress, app
import random
from jinja2 import StrictUndefined
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db
from pprint import pprint
import os
import json
from twilio.rest import Client
from sqlalchemy import update
import doctest

app = Flask(__name__)

app.secret_key = os.environ["SERVER_APP_SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    if 'user_id' in session:
        user = User.query.get(session["user_id"])
        return render_template("homepage.html", user=user)
    else:
        return render_template("homepage.html")


@app.route('/login', methods=["POST"])
def check_login():
    """login existing users"""

    user_name = request.form.get("name").strip().capitalize()
    password = request.form.get("password")

    user = User.query.filter(User.user_name == user_name).first()

    #doubles up - just reference user object above
    user_id = db.session.query(User.user_id).filter(User.user_name == user_name).first()

    if user:
        password_match = db.session.query(User.password).filter(User.user_name == user_name).first()
        password_match = password_match[0]
        if password == password_match:
            session["user_id"] = user_id[0]
            flash(f"Welcome, {user.user_name.title() }!", category='info')
            return redirect(f"/user_info/{user.user_id}")
        else:
            flash("Login failed. Please double-check your password.", category='warning')
            return redirect("/")
    else:
        flash("Looks like you're not registered.  Please register.", category='warning')
        return redirect("/")


@app.route('/logout')
def logout():
    """Clears user_id from session"""
    if 'user_id' in session:
        del session['user_id']
        flash("Logged out.", category='info')
        return redirect("/")
    else:
        flash("Please login.", category='info')
        return redirect("/")


@app.route("/register", methods=["POST"])
def register_new_user():
    """adds new user to the db"""

    user_name = request.form.get("name").strip().title()
    password = request.form.get("password")

    user = User.query.filter(User.user_name == user_name).first()

    if user:
        flash("That user_name is already registered.  Please choose another name.", category='warning')
        return redirect('/')
    else:
        user_name = User(user_name=user_name, password=password)
        db.session.add(user_name)
        db.session.commit()
        flash("Thank you for registering.  Please login to get started!", category='success')
        return redirect("/")


@app.route(f"/user_info/<user_id>")
def user_info(user_id):
    """lists students associated with the user"""

    if "user_id" not in session:
        flash("Please log in.", category='warning')
        return redirect('/login')

    user = User.query.get(user_id)

    return render_template("user_info.html", user=user)


@app.route("/student_history/<student_id>")
def student_history(student_id):
    """displays student progress-report history"""

    #get student object
    student = Student.query.get(student_id)

    user = User.query.get(session["user_id"])

    #get progress object for student (in a list of progress objects).  Loop through these in Jinja and call specific attributes.
    progress = Progress.query.filter(Progress.student_id == student.student_id).order_by(Progress.date.desc()).all()

    # create dictionary that groups progress objects by the behavior name.
    behaviors = {}

    for report in progress:
        # behaviors[report.behavior.behavior_name] = {}
        report.date = report.date.strftime("%B %d, %Y")
        if report.behavior.behavior_name not in behaviors.keys():
            # behaviors[report.behavior.behavior_name] = inner_dict
            behaviors[report.behavior.behavior_name] = [report]
        else:
            behaviors[report.behavior.behavior_name].append(report)

    #create dictionary with data formatted for charts.js
    chart_data = {}
    colors = ['#3366CC','#DC3912','#FF9900','#109618','#990099','#3B3EAC','#0099C6','#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC']
    for report in progress:
        if report.behavior.behavior_name not in chart_data.keys():
            chart_data[report.behavior.behavior_name] = {
                          'labels' : ['Jan', 'Feb', 'March', 'April', 'May', 'June',
                                      'July', 'August', 'Sept', 'Oct', 'Nov', 'Dec',],
                          'background_color' : random.choice(colors),
                          'border_color' : random.choice(colors),
                          'data' : [report.rating]}
            colors.remove(chart_data[report.behavior.behavior_name]['background_color'])
        else:
            chart_data[report.behavior.behavior_name]['data'].append(report.rating)
            chart_data[report.behavior.behavior_name]['data'] = chart_data[report.behavior.behavior_name]['data'][:8]

    chart_json = json.dumps(chart_data, default=str)

    #gets list of all intervention objects from db:
    interventions = db.session.query(Intervention).all()

    #gets list of all behavior objects from db:
    behaviors_list = db.session.query(Behavior).all()

    return render_template("student_history.html", student=student, progress=progress,
                            behaviors=behaviors, chart_json=chart_json,
                            interventions=interventions, behaviors_list=behaviors_list, user=user)


@app.route("/student_history/<student_id>/behavior_history")
def behavior_history(student_id):
    """displays history of specific behavior"""

    behavior_name = request.args.get("behavior_name")
    behavior = Behavior.query.filter(Behavior.behavior_name==behavior_name).first()
    behavior_id = behavior.behavior_id

    user = User.query.get(session["user_id"])

    #creates an iterable list from behavior_description
    behavior_description = behavior.behavior_description.strip('"{}"').split('","')

    #get student object:
    student = Student.query.get(student_id)

    #get progress objects matching the specified behavior for student:
    progress = Progress.query.filter(Progress.student_id==student.student_id, Progress.behavior_id==behavior_id).order_by(Progress.date.desc()).all()

    #create dictionary with data formatted for charts.js
    behavior_progress = {}
    # colors = ['red', 'yellow', 'blue', 'green', 'orange', 'purple']
    colors = ['#3366CC','#DC3912','#FF9900','#109618','#990099','#3B3EAC','#0099C6','#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC']
    ratings = []
    for report in progress:
        if report.behavior.behavior_name not in behavior_progress.keys():
            behavior_progress[report.behavior.behavior_name] = {
                'background_color': random.choice(colors),
                'border_color': random.choice(colors),
                'data': [report.rating]}
        else:
            behavior_progress[report.behavior.behavior_name]['data'].append(report.rating)
            behavior_progress[report.behavior.behavior_name]['data'] = behavior_progress[report.behavior.behavior_name]['data'][:8]

    behavior_progress_json = json.dumps(behavior_progress, default=str)

    #gets list of all intervention objects from db:
    interventions = db.session.query(Intervention).all()

    #gets list of all behavior objects from db:
    behaviors_list = db.session.query(Behavior).all()


    return render_template("behavior_history.html", progress=progress, student=student, behavior=behavior,
                            behavior_description=behavior_description, behavior_progress_json=behavior_progress_json,
                            interventions=interventions, behaviors_list=behaviors_list, user=user)


@app.route("/student_list")
def student_list():
    """displays results from student search"""

    user = User.query.get(session["user_id"])
    user_id = user.user_id

    # debugger to use when testing to freeze because you can't print:
    # import pdb; pdb.set_trace()

    #gets information from student_search form
    fname = request.args.get("fname").capitalize()
    lname = request.args.get("lname").capitalize()
    student_id = request.args.get("student_id")
    birthdate = request.args.get("birthdate")

    #checks to see what info the user entered and generates list of objects that Jinja will loop through.
    if student_id:
        if int(student_id) > 5000000:
            flash("Please try again.  That name/ID is not found", category='info')
            return redirect(f"/user_info/{user_id}")
        student = Student.query.filter(Student.student_id==student_id).all()
        if not student:
            flash("Please try again.  That name/ID is not found", category='info')
            return redirect(f"/user_info/{user_id}")
    elif birthdate:
        student = Student.query.filter(Student.birthdate==birthdate).all()
        if not student:
            flash("Please try again.  That name/ID is not found", category='info')
            return redirect(f"/user_info/{user_id}")
    elif fname and lname:
        student = Student.query.filter(Student.fname==fname, Student.lname==lname).all()
        if not student:
            flash("Please try again.  That name/ID is not found", category='info')
            return redirect(f"/user_info/{user_id}")
    elif fname and (not lname):
        student = Student.query.filter(Student.fname==fname).all()
        if not student:
            flash("Please try again.  That name/ID is not found", category='info')
            return redirect(f"/user_info/{user_id}")
    elif lname and (not fname):
        student = Student.query.filter(Student.lname==lname).all()
        if not student:
            flash("Please try again.  That name/ID is not found", category='info')
            return redirect(f"/user_info/{user_id}")
    else:
        flash("Please try again.  That name/ID is not found", category='info')
        return redirect(f"/user_info/{user_id}")


    return render_template("student_list.html", student=student, user=user)


@app.route("/add_progress/<student_id>", methods=["POST"])
def add_progress(student_id):
    """adds new progress report to db"""

    interventions = db.session.query(Intervention).all()
    behaviors = db.session.query(Behavior).all()

    #create dictionary of intervention id key with intervention name as value
    intervent_name = {}
    for intervention in interventions:
        intervent_name[intervention.intervention_id] = intervention.intervention_name

    date = request.form.get("date")
    behavior_id = request.form.get('behave')
    intervention_id = request.form.get("intervent")
    user_id = session["user_id"]
    rating = request.form.get("rating")
    comment = request.form.get("comment")

    if date is '':
        flash("Please select a date.", category='danger')
        return redirect(f"/student_history/{student_id}")

    #get progress objects matching the specified behavior for student:
    behavior_progress = Progress.query.filter(Progress.student_id==student_id, Progress.behavior_id==behavior_id).order_by(Progress.intervention_id).all()

    #creates a dictionary sorting progress reports by behavior.
    progress_dict = {}
    for progress in behavior_progress:
        if progress.behavior_id not in progress_dict:
            progress_dict[progress.behavior_id] = {'Date': [progress.date],
                                                   'Intervention': [progress.intervention_id],
                                                   'Rating': [progress.rating],
                                                   'Comment': [progress.comment]}
        else:
            progress_dict[progress.behavior_id]['Date'].append(progress.date)
            progress_dict[progress.behavior_id]['Intervention'].append(progress.intervention_id)
            progress_dict[progress.behavior_id]['Rating'].append(progress.rating)
            progress_dict[progress.behavior_id]['Comment'].append(progress.comment)

    # creates a dictionary with intervention_ids as key and number of times they've been used as values.
    intervents = {}
    for progress in behavior_progress:
        if progress.intervention_id in intervents:
            intervents[progress.intervention_id] = intervents[progress.intervention_id] + 1
        else:
            intervents[progress.intervention_id] = 1

    #checks the number of progress reports with that intervention and reccomends an evaluation after 6 progress reports.
    if intervents == {}:
        progress = Progress(student_id=student_id, date=date, behavior_id=behavior_id,
                            intervention_id=intervention_id, user_id=user_id, rating=rating,
                            comment=comment)
        db.session.add(progress)
        db.session.commit()

        return redirect(f"/student_history/{student_id}")

    elif (int(intervention_id) not in intervents.keys()):
        # if the intervention id is in the dictionary, check and see how many times it's been used.
        for item in intervents:
            # if other interventions have been tried <6 times, don't add the new intervention.
            if intervents[item] < 6:
                flash(f"""You've only tried '{intervent_name[item]}' {intervents[item]} times. \n
                       We reccommend applying the same intervention to the targeted behavior at
                       least 6 times before changing interventions.""", category='danger')
                return redirect(f"/student_history/{student_id}")
            else:
                # if other interventions have been tried >6 times, add this new intervention.
                progress = Progress(student_id=student_id, date=date, behavior_id=behavior_id,
                                    intervention_id=intervention_id, user_id=user_id, rating=rating, comment=comment)
                db.session.add(progress)
                db.session.commit()
                return redirect(f"/student_history/{student_id}")

    elif (int(intervention_id) in intervents.keys()):
    # if intervention_id is in the dictionary update it to add progress report to database.
        # if int(intervents[intervention_id]) > 6:
        # flash(f"You've tried this intervention {intervents[intervention_id]} times.  It's a good time to evaluate progress.")
        progress = Progress(student_id=student_id, date=date, behavior_id=behavior_id,
                            intervention_id=intervention_id, user_id=user_id, rating=rating,
                            comment=comment)
        db.session.add(progress)
        db.session.commit()

        return redirect(f"/student_history/{student_id}")


@app.route("/add_student", methods=["POST"])
def add_student():
    """adds a new student to the db"""

    fname = request.form.get("fname").strip().capitalize()
    lname = request.form.get("lname").strip().capitalize()
    user_id = session["user_id"]
    birthdate = request.form.get("birthdate")
    phone_number = request.form.get("phone")
    photo = request.form.get("photo")

    if (fname is '') or (lname is '') or (phone_number is '') or (birthdate is ''):
        flash("Please complete all fields of the student profile.", category='danger')
        return redirect(f"/user_info/{user_id}")

    student = Student(fname=fname, lname=lname, user_id=user_id, birthdate=birthdate, phone_number=phone_number, photo=photo)
    db.session.add(student)
    db.session.commit()
    return redirect(f"/user_info/{user_id}")


@app.route("/interventions")
def display_interventions():
    """displays a list of optional interventions"""

    interventions = db.session.query(Intervention).order_by(Intervention.intervention_name).all()
    names = db.session.query(Intervention.intervention_name).order_by(Intervention.intervention_name).all()
    behaviors = db.session.query(Behavior).order_by(Behavior.behavior_name).all()

    user = User.query.get(session["user_id"])

    #creates an iterable list from behavior_description
    for behavior in behaviors:
        behavior.behavior_description = behavior.behavior_description.strip('"{}"').split('","')

    #create dictionary of intervention name key with intervention id as value (for typeahead-modal functionality)
    int_id = {}
    for intervention in interventions:
        int_id[intervention.intervention_name] = intervention.intervention_id

    int_id_json = json.dumps(int_id)

    intervention_names= []
    for name in names:
        intervention_names.append(name[0])

    interventions_json = json.dumps(intervention_names)

    return render_template("interventions.html", interventions=interventions,
                            interventions_json=interventions_json, behaviors=behaviors,
                            int_id_json=int_id_json, user=user)


@app.route("/add_intervention", methods=["POST"])
def add_intervention():
    """adds new intervention to the database"""

    intervention_name = request.form.get("intervention_name").strip().capitalize()
    intervention_behaviors = request.form.get("intervention_behaviors").split(",")

    related_behaviors = []
    for i in intervention_behaviors:
        i = i.strip(" ").capitalize()
        related_behaviors.append(i)

    user_id = session["user_id"]

    if len(intervention_behaviors) > 400:
        intervention_behaviors = intervention_behaviors[:400]

    #make list of all the behaviors already in the database
    interventions = db.session.query(Intervention.intervention_name).all()
    intervention_list = []
    for intervention in interventions:
        intervention_list.append((intervention[0]))

    #make sure user is not able to add a duplicate behavior.
    if intervention_name in intervention_list:
        flash("That intervention is already an option.", category='info')
        return redirect("/interventions")

    #make sure all the fields are filled out:
    if intervention_name is None:
        flash("Please enter an intervention name", category='danger')
        return redirect("/add_intervention")

    intervention = Intervention(intervention_name=intervention_name)
    db.session.add(intervention)

    for behavior in related_behaviors:
        if db.session.query(Behavior).filter(Behavior.behavior_name==behavior).first():
            behavior = db.session.query(Behavior).filter(Behavior.behavior_name==behavior).first()
            intervention.behaviors.append(behavior)

    db.session.commit()

    return redirect('/interventions')


@app.route("/behaviors")
def display_behaviors():
    """displays a list of optional behaviors"""

    behaviors = db.session.query(Behavior).order_by(Behavior.behavior_name).all()
    user = User.query.get(session["user_id"])

    #creates an iterable list from behavior_description
    for behavior in behaviors:
        behavior.behavior_description = behavior.behavior_description.strip('"{}"').split('","')

    b_names = db.session.query(Behavior.behavior_name).order_by(Behavior.behavior_name).all()

    #create dictionary of behavior name key with behavior id as value (for typeahead-modal functionality)
    b_id = {}
    for behavior in behaviors:
        b_id[behavior.behavior_name] = behavior.behavior_id

    b_id_json = json.dumps(b_id)

    behavior_names = []
    for name in b_names:
        behavior_names.append(name[0])

    behaviors_json = json.dumps(behavior_names)

    return render_template("behaviors.html", behaviors=behaviors,
                           behaviors_json=behaviors_json, b_id_json=b_id_json, user=user)


@app.route("/behavior_info/<behavior_id>")
def behavior_info(behavior_id):
    """displays info about a specific behavior"""

    #get behavior object
    behavior = Behavior.query.get(behavior_id)

    #creates an iterable list from behavior.behavior_description
    description = behavior.behavior_description.strip('"{}"').split('","')

    #gets an iterable list of related intervention names for the behavior
    associated_interventions =[]
    for intervention in behavior.interventions:
        associated_interventions.append(intervention.intervention_name)

    user_id = session["user_id"]

    return render_template("behavior_info.html", behavior=behavior,
                           description=description, associated_interventions=associated_interventions)


@app.route("/add_behavior", methods=["POST"])
def add_behavior():
    """adds new behavior to the database"""

    behavior_name = request.form.get("behavior_name").strip().capitalize()
    behavior_d = request.form.get("behavior_description").split(",")
    associated_interventions = request.form.get("associated_interventions").split(",")

    behavior_description = []
    for behavior in behavior_d:
        behavior = behavior.strip(" ").capitalize()
        behavior_description.append(behavior)

    related_interventions = []
    for i in associated_interventions:
        i = i.strip(" ").capitalize()
        related_interventions.append(i)

    user_id = session["user_id"]

    if len(behavior_description) > 1000:
        behavior_description = behavior_description[:1000]

    #make list of all the behaviors already in the database
    behaviors = db.session.query(Behavior.behavior_name).all()
    behavior_list = []
    for behavior in behaviors:
        behavior_list.append((behavior[0]))

    #make sure user is not able to add a duplicate behavior.
    if behavior_name in behavior_list:
        flash("That behavior is already an option.", category='info')
        return redirect("/behaviors")

    #make sure all the fields are filled out:
    if behavior_name is None:
        flash("Please enter a behavior name", category='danger')
        return redirect("/add_behavior")
    if behavior_d is None:
        flash("Please enter a behavior description", category='danger')
        return redirect("/add_behavior")

    behavior = Behavior(behavior_name=behavior_name, behavior_description=behavior_description)
    db.session.add(behavior)

    for intervention in related_interventions:
        if db.session.query(Intervention).filter(Intervention.intervention_name==intervention).first():
            intervention = db.session.query(Intervention).filter(Intervention.intervention_name==intervention).first()
            behavior.interventions.append(intervention)

    db.session.commit()

    return redirect('/behaviors')


@app.route("/send_progress/<student_id>")
def send_progress(student_id):
    """sends progress report to parent"""

    # get student object
    student = Student.query.get(student_id)

    # Gets the number saved for student in the database
    phone_number = student.phone_number.strip("- ")

    if phone_number != "3132589798":
        flash("""This feature is currently only available for verified phone numbers.\n
                  Please check back later or contact the site administrator.""", category='info')
        return redirect(f"/student_history/{student_id}")
    # Gets the message and report from the form
    comment = request.args.get("comment")
    report = request.args.get("report")
    report = "Progress Report Update: " + comment + " " + report

    account_sid = os.environ["ACCOUNT_SID_KEY"]
    auth_token = os.environ["AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    user_id = session["user_id"]

    message = client.messages.create(
                              body=report,
                              from_='+12486218673',
                              to=phone_number
                              )

    print(message.sid)
    return redirect(f"/student_history/{student_id}")


@app.route("/edit_student/<student_id>", methods=["POST"])
def edit_student_profile(student_id):
    """allows user to edit student profile"""

    # get student object
    student = Student.query.get(student_id)

    fname = request.form.get("fname").capitalize()
    phone_number = request.form.get("phone_number").strip("- ")
    birthdate = request.form.get("birthdate")
    photo = request.form.get("photo")

    # check to see if form is filled out or keep previous values.
    if fname:
        student.fname = fname
    else:
        student.fname = student.fname

    if phone_number:
        student.phone_number = phone_number.strip("- ")
    else:
        student.phone_number = student.phone_number

    if birthdate == '':
        student.birthdate = student.birthdate
    else:
        student.birthdate = birthdate

    if photo:
        student.photo = photo
    else:
        student.photo = student.photo

    db.session.commit()

    return redirect(f"/student_history/{student_id}")


@app.route("/edit_user/<user_id>", methods=["POST"])
def edit_user_profile(user_id):
    """allows user to edit user profile"""

    # get user object
    user = User.query.get(user_id)

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password").strip(" ")

    # check to see if current password is correct:
    if current_password == user.password:
        user.password = new_password
        db.session.commit()
        return redirect(f"/user_info/{user_id}")
    else:
        flash("Your current password does not match our records.  Please try again.", category='danger')
        return redirect(f"/user_info/{user_id}")


if __name__ == "__main__":
    # Set debug=True, it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # #DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")