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

app = Flask(__name__)

app.secret_key = os.environ["SERVER_APP_SECRET_KEY"]

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
            flash("Welcome!")
            return redirect(f"/user_info/{user.user_id}")
        else:
            flash("Login failed. Please double-check your password.")
            return redirect("/")
    else:
        flash("Looks like you're not registered.  Please register.")
        return redirect("/")


@app.route('/logout')
def logout():
    """Clears user_id from session"""
    if 'user_id' in session:
        del session['user_id']
        flash("Logged out.")
        return redirect("/")
    else:
        flash("Please login")
        return redirect("/")


@app.route('/register')
def user_register():
    """Gets email and password from user"""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_new_user():
    """adds new user to the db"""

    user_name = request.form.get("name").strip().capitalize()
    password = request.form.get("password")

    user = User.query.filter(User.user_name == user_name).first()

    if user:
        flash("That user_name is already registered.  Please choose another name.")
        return redirect('/')
    else:
        user_name = User(user_name=user_name, password=password)
        db.session.add(user_name)
        db.session.commit()
        flash("Thank you for registering.  Please login to get started!")
        return redirect("/")


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
    student.birthdate = student.birthdate.strftime("%B %d, %Y")

    user_id = session["user_id"]

    #get progress object for student (in a list of progress objects).  Loop through these in Jinja and call specific attributes.
    progress = Progress.query.filter(Progress.student_id == student.student_id).order_by(Progress.date.desc()).all()

    # #in this nested dictionary, each of the student's behaviors is a dictionary key with a nested dictionary
    # #that contains list of progress report dates as the value of 'dates' and a list of corresponding progress ratings
    # #as the values of 'ratings'.
    behaviors = {}
    inner_dict = {}

    for report in progress:
        # behaviors[report.behavior.behavior_name] = {}
        report.date = report.date.strftime("%B %d, %Y")
        if report.behavior.behavior_name not in behaviors.keys():
            # behaviors[report.behavior.behavior_name] = inner_dict
            behaviors[report.behavior.behavior_name] = {'reports': [(report.date, report.rating, report.comment)]}
        else:
            behaviors[report.behavior.behavior_name]['reports'].append((report.date, report.rating, report.comment))


    # b_p_l = []
    # i = 0
    # while i < len(behaviors):
    #     for behavior in behaviors:
    #         b_p = (behaviors[behavior]['dates'][i], behaviors[behavior]['ratings'][i], behaviors[behavior]['comments'][i])
    #         b_p_l.append(b_p)
    #         i += 1

    # print(b_p_l)
    print("<<<<<<<<<<<<")
    print(behaviors)
    print("<<<<<<<<<<<<")


    #create dictionary with data formatted for charts.js
    chart_data = {}
    colors = ['red', 'yellow', 'green', 'blue', 'orange', 'purple']
    for report in progress:
        if report.behavior.behavior_name not in chart_data.keys():
            chart_data[report.behavior.behavior_name] = {
                          'labels' : ['Jan', 'Feb', 'March', 'April', 'May', 'June',
                                      'July', 'August', 'Sept', 'Oct', 'Nov', 'Dec',],
                          'background_color' : random.choice(colors),
                          'border_color' : random.choice(colors),
                          'data' : [report.rating]}
        else:
            chart_data[report.behavior.behavior_name]['data'].append(report.rating)
        chart_data[report.behavior.behavior_name]['data'] = chart_data[report.behavior.behavior_name]['data'][:8]

    chart_json = json.dumps(chart_data, default=str)

    #gets list of all intervention objects from db:
    interventions = db.session.query(Intervention).all()

    #gets list of all behavior objects from db:
    behaviors_list = db.session.query(Behavior).all()

    return render_template("student_history.html", student=student, progress=progress,
                            user_id=user_id, behaviors=behaviors, chart_json=chart_json,
                            interventions=interventions, behaviors_list=behaviors_list)


@app.route("/student_history/<student_id>/behavior_history")
def behavior_history(student_id):
    """displays history of specific behavior"""

    behavior_name = request.args.get("behavior_name")
    behavior = Behavior.query.filter(Behavior.behavior_name==behavior_name).first()
    behavior_id = behavior.behavior_id

    #creates an iterable list from behavior_description
    behavior_description = behavior.behavior_description.strip('"{}"').split('","')

    #get student object:
    student = Student.query.get(student_id)
    # birthdate = student.birthdate.strftime("%B %d, %Y")

    #get progress objects matching the specified behavior for student:
    progress = Progress.query.filter(Progress.student_id==student.student_id, Progress.behavior_id==behavior_id).order_by(Progress.date.desc()).all()
    # date = progress.date.strftime("%B %d, %Y")

    #create dictionary with data formatted for charts.js
    behavior_progress = {}
    colors = ['red', 'yellow', 'blue', 'green', 'orange', 'purple']
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
                            interventions=interventions, behaviors_list=behaviors_list)


@app.route("/student_search")
def student_search_form():
    """gets students search info from user"""

    return render_template("student_search.html")


@app.route("/student_list")
def student_list():
    """displays results from student search"""

    #gets information from student_search form
    fname = request.args.get("fname").capitalize()
    lname = request.args.get("lname").capitalize()
    student_id = request.args.get("student_id")
    birthdate = request.args.get("birthdate")

    #checks to see what info the user entered and generates list of objects that Jinja will loop through.
    if student_id:
        student = Student.query.filter(Student.student_id==student_id).all()
    elif birthdate:
        student = Student.query.filter(Student.birthdate==birthdate).all()
    elif fname and lname:
        student = Student.query.filter(Student.fname==fname, Student.lname==lname).all()
    elif fname and (not lname):
        print(fname)
        student = Student.query.filter(Student.fname==fname).all()
    elif lname and (not fname):
        print(lname)
        student = Student.query.filter(Student.lname==lname).all()
    else:
        flash("Please try again.  That name/ID is not found")
        return redirect("/student_search")

    return render_template("student_list.html", student=student)


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

    #create dictionary of intervention id key with intervention name as value
    intervent_name = {}
    for intervention in interventions:
        intervent_name[intervention.intervention_id] = intervention.intervention_name

    # ADD IN CHECKS TO MAKE SURE ALL FIELDS ARE FILLED OUT
    date = request.form.get("date")
    behavior_id = request.form.get('behave')
    intervention_id = request.form.get("intervent")
    user_id = session["user_id"]
    rating = request.form.get("rating")
    comment = request.form.get("comment")

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
    if int(intervention_id) not in intervents.keys():
        print("IT'S NOT IN THE DICTIONARY!")
        # if the intervention id is in the dictionary, check and see how many times it's been used.
        for item in intervents:
            # if other interventions have been tried <6 times, don't add the new intervention.
            if intervents[item] < 6:
                flash(f"You've only tried '{intervent_name[item]}' {intervents[item]} times.")
                flash("We reccommend applying the same intervention to the targeted behavior at least 6 times before changing interventions.")
                return redirect(f"/student_history/{student_id}")
            else:
                # if other interventions have been tried >6 times, add this new intervention.
                progress = Progress(student_id=student_id, date=date, behavior_id=behavior_id,
                                    intervention_id=intervention_id, user_id=user_id, rating=rating, comment=comment)
                db.session.add(progress)
                db.session.commit()
                return redirect(f"/student_history/{student_id}")

    elif int(intervention_id) in intervents.keys():
    # if intervention_id is in the dictionary update it to add progress report to database.
        # if int(intervents[intervention_id]) > 6:
        #     flash(f"You've tried this intervention {intervents[intervention_id]} times.  It's a good time to evaluate progress.")
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

    fname = request.form.get("fname").strip().capitalize()
    lname = request.form.get("lname").strip().capitalize()
    user_id = session["user_id"]
    birthdate = request.form.get("birthdate")

    student = Student(fname=fname, lname=lname, user_id=user_id, birthdate=birthdate)
    db.session.add(student)
    db.session.commit()
    return redirect(f"/user_info/{user_id}")


@app.route("/interventions")
def display_interventions():
    """displays a list of optional interventions"""

    interventions = db.session.query(Intervention).order_by(Intervention.intervention_name).all()
    names = db.session.query(Intervention.intervention_name).order_by(Intervention.intervention_name).all()
    behaviors = db.session.query(Behavior).order_by(Behavior.behavior_name).all()

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
                            int_id_json=int_id_json)


@app.route("/new_intervention")
def show_intervention_info():
    """gets new intervention info from user"""

    return render_template('new_intervention.html')


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
        flash("That intervention is already an option.")
        return redirect("/interventions")

    #make sure all the fields are filled out:
    if intervention_name is None:
        flash("Please enter an intervention name")
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
                           behaviors_json=behaviors_json, b_id_json=b_id_json)


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


@app.route("/new_behavior")
def show_behavior_info():
    """gets new behavior info from user"""

    return render_template('new_behavior.html')


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
        flash("That behavior is already an option.")
        return redirect("/behaviors")

    #make sure all the fields are filled out:
    if behavior_name is None:
        flash("Please enter a behavior name")
        return redirect("/add_behavior")
    if behavior_d is None:
        flash("Please enter a behavior description")
        return redirect("/add_behavior")

    behavior = Behavior(behavior_name=behavior_name, behavior_description=behavior_description)
    db.session.add(behavior)

    for intervention in related_interventions:
        if db.session.query(Intervention).filter(Intervention.intervention_name==intervention).first():
            intervention = db.session.query(Intervention).filter(Intervention.intervention_name==intervention).first()
            behavior.interventions.append(intervention)

    db.session.commit()

    return redirect('/behaviors')


@app.route("/send_progress")
def send_progress():
    """sends progress report to parent"""

    account_sid = os.environ["ACCOUNT_SID_KEY"]
    auth_token = os.environ["AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    user_id = session["user_id"]

    message = client.messages.create(
                              body='Hello there!',
                              from_='+12486218673',
                              to='+13132589798'
                            )

    print(message.sid)


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