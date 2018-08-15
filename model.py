
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


def connect_to_db(app):
    """Connect database to Flask app."""

    #Configure to use the PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///behavior'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

app = Flask(__name__)

if __name__ == "__main__":
    """If run interactively will allow you to work with db directly"""

    # from server import app
    connect_to_db(app)
    print("Connected to DB.")


class User(db.Model):
    """user information"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    students = db.relationship("Student")
    progress = db.relationship("Progress")

    def __repr__(self):
        """show info about the user"""

        return """<user_id = {}, user_name = {}>""".format(self.user_id, self.user_name)


class Student(db.Model):
    """student information"""

    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    # twilio api will only send sms to valid phone numbers - so for demo my number is connected to all students.
    phone_number = db.Column(db.String(15), nullable=False)
    photo = db.Column(db.String(400), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    progress = db.relationship("Progress")
    user = db.relationship("User")

    def __repr__(self):
        """show info about the student"""

        return """<student_id = {},
                  first name = {},
                  last name = {},
                  birthdate = {}>""".format(self.student_id, self.fname, self.lname, self.birthdate)


class Behavior(db.Model):
    """behavior information"""

    __tablename__ = 'behaviors'

    behavior_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    behavior_name = db.Column(db.String(200), nullable=False)
    behavior_description = db.Column(db.String(1000), nullable=False)
    behavior_interventions = db.Column(db.String(400), nullable=True)

    progress = db.relationship("Progress")
    #creates a relatipnship with students via the progress table,
    #to see all students w that behavior.
    students = db.relationship("Student", secondary="progress")
    interventions = db.relationship("Intervention", secondary="behavior_interventions", backref="behaviors")

    def __repr__(self):
        """show info about the behavior"""

        return """<behavior_id = {},
                  behavior_name = {},
                  behavior_description = {}>""".format(self.behavior_id,
                                                       self.behavior_name,
                                                       self.behavior_description)


class Intervention(db.Model):
    """intervention information"""

    __tablename__ = 'interventions'

    intervention_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    intervention_name = db.Column(db.String(500), nullable=False)
    intervention_behaviors = db.Column(db.String(400), nullable=True)

    #creates a relationship with students, through the progress table
    # student = db.relationship("Student", secondary="progress")

    progress = db.relationship("Progress")
    #THIS IS WHERE YOU MAY BE Fing EVERYTHING UP.
    # behaviors = db.relationship("Behavior", secondary="behavior_interventions", backref="interventions")

    def __repr__(self):
        """show info about the intervention"""

        return """<intervention_id = {},
                  intervention_name,
                  intervention_description = {}>""".format(self.intervention_id,
                                                           self.intervention_name,
                                                           self.intervention_behaviors)


class BehaviorIntervention(db.Model):
    """connects behaviors table to interventions table"""

    __tablename__ = 'behavior_interventions'

    association_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    behavior_id = db.Column(db.Integer, db.ForeignKey("behaviors.behavior_id"), nullable=False)
    intervention_id = db.Column(db.Integer, db.ForeignKey("interventions.intervention_id"), nullable=False)

    def __repr__(self):
        """shows info on connection between behavior and interventions"""

        return """<association_id = {}, behavior_id = {},
                   intervention_id = {}>""".format(self.association_id, self.behavior_id, self.intervention_id)



class Progress(db.Model):
    """progress information"""

    __tablename__ = "progress"

    progress_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    behavior_id = db.Column(db.Integer, db.ForeignKey('behaviors.behavior_id'), nullable=False)
    intervention_id = db.Column(db.Integer, db.ForeignKey('interventions.intervention_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))

    intervention = db.relationship("Intervention", backref="progresses")
    behavior = db.relationship("Behavior", backref="progresses")
    student = db.relationship("Student", backref="progresses")
    user = db.relationship("User")

    def __repr__(self):
        """show info about student progress"""

        return """<progress_id = {},
                   student_id = {},
                   date = {},
                   behavior = {},
                   intevention= {},
                   user_id = {},
                   rating = {},
                   comment = {}>""".format(self.progress_id,
                                           self.student_id,
                                           self.date,
                                           self.behavior_id,
                                           self.intervention_id,
                                           self.user_id,
                                           self.rating,
                                           self.comment)
