
from sqlalchemy import func
from model import User, Student, Behavior, Intervention, Progress, app
import random
from datetime import datetime

from model import connect_to_db, db


def load_students():
    """load students from u.student into database."""

    user = User(user_name="Jane Doe", password="ubermelon")

    db.session.add(user)

    first_names = ['Jane', 'Nancy', 'Billy', 'Victor', 'Ted']
    last_names = ['Schmoe', 'Doe', 'Crystal', 'Nelson', 'Smith']

    for fname in first_names:
        fname = random.choice(first_names)
        for lname in last_names:
            lname = random.choice(last_names)

            student = Student(fname=fname, lname=lname, user_id=user.user_id)
            db.session.add(student)

            user.students.append(student)

    db.session.commit()


def load_behaviors():
    """load behaviors from u.behavior into database"""

    b_dict = {'talks out': 'speaks loudly, does not raise hand, shouts',
              'distracted': 'out of seat, staring into space, talking to others',
              'bully': 'jerk, fights, name calls',
              'sleeps': 'head on desk, snoring, eyes closed',
              'cheats': 'copies others work, turns in fake work, denies cheating'}

    for behavior in b_dict:
        behavior_name = list(b_dict.keys())
        behavior_name = random.choice(behavior_name)
        print(behavior_name)
        behavior_description = b_dict[behavior_name]
        print(behavior_description)

        behavior = Behavior(behavior_name=behavior_name,
                            behavior_description=behavior_description)

        db.session.add(behavior)

    db.session.commit()


def load_interventions():
    """load interventions from u.intervention into database"""

    i_dict = {'Avoid power struggles': 'Admit if you made a mistake, provide choice',
              'Explain assignment': 'Provide explicit sequential instruction in writing and verbally',
              'Acknowledging positive behavior': 'Provide reward or praise (public or private)'}

    for intervention in i_dict:
        intervention_name = list(i_dict.keys())
        intervention_name = random.choice(intervention_name)
        intervention_description = i_dict[intervention_name]

        intervention = Intervention(intervention_name=intervention_name,
                                    intervention_description=intervention_description)
        db.session.add(intervention)

    db.session.commit()


def load_progress():
    """load progress from u.progress into database"""

    #generates random rating
    # rating = random.randint(0, 10)

    #generates random comment from list
    comments = ["great progress", "no progress yet", "still happens, but not as much as initially",
                "friend was moved to other class, behavior improved", "snickers bribe helps!"]

    # comment = random.choice(comments)

    #generates random date
    # year = random.randint(2016, 2019)
    # month = random.randint(1, 12)
    # day = random.randint(1, 28)
    # date = datetime(year, month, day)

    #generates random student_id
    all_students = db.session.query(Student.student_id).all()
    # student_id = random.choice(all_students)

    #generates random behavior_id
    all_behaviors = db.session.query(Behavior.behavior_id).all()
    # behavior_id = random.choice(all_behaviors)

    #generates random intervention_id
    all_interventions = db.session.query(Intervention.intervention_id).all()
    # intervention_id = random.choice(all_interventions)

    #generates random user_id
    all_users = db.session.query(User.user_id).all()
    # user_id = random.choice(all_users)

    i = 1
    while i < len(all_students):
        student_id = random.choice(all_students)
        behavior_id = random.choice(all_behaviors)
        intervention_id = random.choice(all_interventions)
        year = random.randint(2016, 2019)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = datetime(year, month, day)
        user_id = random.choice(all_users)
        rating = random.randint(0, 10)
        comment = random.choice(comments)

        progress = Progress(student_id=student_id, behavior_id=behavior_id,
                            intervention_id=intervention_id, date=date,
                            user_id=user_id, rating=rating, comment=comment)
        i +=1

        db.session.add(progress)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_students()
    load_behaviors()
    load_interventions()
    load_progress()
