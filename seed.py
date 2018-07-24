
from sqlalchemy import func
from model import User, Student, Behavior, Intervention, Progress, app
import random
from datetime import datetime

from model import connect_to_db, db


def load_students():
    """load students from u.student into database."""

    user = User("Jane Doe")

    first_names = ['Jane', 'Nancy', 'Billy', 'Victor', 'Ted']
    last_names = ['Schmoe', 'Doe', 'Crystal', 'Nelson', 'Smith']

    for fname in first_names:
        fname = random.choice(first_names)

        for lname in last_names:
            lname = random.choice(last_names)

            student = Student(fname=fname, lname=lname, user=user)

            db.session.add(student)

    db.session.commit()

        # dict = [{name:Jane , lname: Hacks},
# Joe | Schmoe
# Nancy | Drew
# Bill | Clinton
# Billy | Crystal]


def load_behaviors():
    """load behaviors from u.behavior into database"""

    b_dict = {'talks out': 'speaks loudly, does not raise hand, shouts',
              'distracted': 'out of seat, staring into space, talking to others',
              'bully': 'jerk, fights, name calls',
              'sleeps': 'head on desk, snoring, eyes closed',
              'cheats': 'copies others work, turns in fake work, denies cheating'}

    for behavior in b_dict:
        behavior_name = random.choice(b_dict.key())
        behavior_description = b_dict[behavior_name]

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
        intervention_name = random.choice(i_dict.key())
        intervention_description = i_dict[intervention_name]

        intervention = Intervention(intervention_name=intervention_name,
                                    intervention_description=intervention_description)
        bd.session.add(intervention)

    db.session.commit()


def load_progress():
    """load progress from u.progress into database"""

    #generates random rating
    rating = random.randint(0, 10)

    #generates random comment from list
    comments = ["great progress", "no progress yet", "still happens, but not as much as initially",
                "friend was moved to other class, behavior improved", "snickers bribe helps!"]

    comment = random.choice(comments)

    #generates random date
    year = random.randomint(2016, 2019)
    month = random.randomint(1, 12)
    day = random.randomint(1, 28)
    date = datetime(year, month, day)

    progress = Progress(date=date, rating=rating, comment=comment)

    db.session.add(progress)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_students()
    load_behaviors()
    load_interventions()
    load_progress()
