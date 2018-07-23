
from flask import Flask 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """user information"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    students = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student")
    progress = db.relationship("Progress")

    def __repr __(self):
        """show info about the user"""

        return "<user_id = {}, students = {}>".format(self.user_id, self.students)

class Student(db.Model):
    """student information"""

    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    # behaviors = db.Column(db.Integer, nullable=False, db.ForeignKey('behaviors.behavior_id'))
    # interventions = db.Column(db.Integer, nullable=False, db.ForeignKey('interventions.intervention_id'))

    progress = db.relationship("Progress")
    user = db.relationship("User")
    # behavior = db.relationship("Behavior")


    def __repr__(self):
        """show info about the student"""

        return "<student_id = {}, first name = {}, last name = {}>"
                 .format(self.student_id, self.fname, self.lname)

class Behavior(db.Model):
    """behavior information"""

    __tablename__ = 'behaviors'

    behavior_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    behavior_name = db.Column(db.String(100), nullable=False)
    behavior_description = db.Column(db.String(200), nullable=False)
    intervention_id = db.Column(db.Integer, nullable=False, db.ForeignKey('interventions.intervention_id'))

    progress = db.relationship("Progress")
    student = db.relationship("Student")
    intervention = db.relationship("Intervention")

    def __repr__(self):
        """show info about the behavior"""

        return "<behavior_id = {}, behavior_name = {}, behavior_description = {}, interventions = {}>"
                 .format(self.behavior_id, self.behavior_name, self.behavior_description, self.interventions)


class Intervention(db.Model):
    """intervention information"""

    __tablename__ = 'interventions'

    intervention_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    behavior_id = db.Column(db.Integer, nullable=False, db.ForeignKey('behaviors.behavior_id'))
    intervention_description = db.Column(db.String(500), nullable=False)

    progress = db.relationship("Progress")
    behavior = db.relationship("Behavior")

    def __repr__(self):
        """show info about the intervention"""

        return "<intervention_id = {}, behaviors = {}, intervention_description = {}>"
                 .format(self.intervention_id, self.behavior_id, self.intervention_description)


class Progress(db.Model):
    """progress information"""

    __tablename__ = "progress"

    progress_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, nullable=False, db.ForeignKey('students.student_id'))
    date = db.Column(db.DateTime, nullable=False)
    behavior_id = db.Column(db.Integer, nullable=False, db.ForeignKey('behaviors.behavior_id'))
    intervention_id = db.Column(db.Integer, nullable=False, db.ForeignKey('interventions.intervention_id'))
    user_id = db.Column(db.Integer, nullable=False, db.ForeignKey('users.user_id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))

    intervention = db.relationship("Intervention")
    behavior = db.relationship("Behavior")
    student = db.relationship("Student")
    user = db.relationship("User")

    def __repr__(self):
        """show info about student progress"""

        return "<progress_id = {}, student_id = {}, date = {}, behavior = {}, intevention= {}, user_id = {}, rating = {}, comment = {}>"
                 .format(self.progress_id, self.student_id, self.date, self.behavior_id, self.intervention_id, self.user_id, self.rating, self.comment)


def connect_to_db(app):
    """Connect database to Flask app."""

    #Configure to use the PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///behaviors'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = FALSE
    db.app = app
    db.init_app(app)

if __name__ = "__main__":
    """If run interactively will allow you to work with db directly"""

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
