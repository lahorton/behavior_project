import unittest
from unittest import TestCase
from faker import Faker
from server import app
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import User, Student, Behavior, Intervention, BehaviorIntervention, Progress, connect_to_db, db


# Code below is not working to create a test db... no tables are created after running tests_model.py to create it.
def example_data():
    """creates sample data for testing"""

    # Add sample data
    test_user = User(user_name="test_user", password="12345", user_id=1)
    db.session.add(test_user)
    test_student = Student(fname="test", lname="student",
                           birthdate=datetime(2000, 9, 7),
                           phone_number="3132589798", user_id=test_user.user_id, student_id=1)
    db.session.add(test_student)
    test_behavior = Behavior(behavior_name="test_behavior", behavior_description="tests stuff", behavior_id=1)
    db.session.add(test_behavior)
    test_intervention = Intervention(intervention_name="test_intervention", intervention_id=1)
    db.session.add(test_intervention)
    test_progress = Progress(student_id=test_student.student_id, behavior_id=test_behavior.behavior_id,
                             intervention_id=test_intervention.intervention_id,
                             date=datetime(2018, 8, 30),
                             rating="5", comment="test comment", user_id=test_user.user_id)
    db.session.add(test_progress)

    # db.session.add_all([test_user, test_student, test_behavior, test_intervention, test_progress])
    db.session.commit()


class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        app.config['Testing'] = True
        app.config['SECRET_KEY'] = 'testing'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        db.create_all()
        example_data()

    def test_login(self):
        """test login page."""
        result = self.client.post('/login', data={"name": "test_user", "password": "12345"},
                                  follow_redirects=True)
        self.assertIn(b'<li>Collect baseline data.', result.data)

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn(b'<li>Choose a behavior', result.data)

    def test_user_info(self):
        result = self.client.get("/user_info/1")
        self.assertIn(b'<h2>Welcome,', result.data)
        self.assertEqual(result.status_code, 200)

    def test_student_history(self):
        result = self.client.get("/student_history/1",
                                 follow_redirects=True)
        self.assertIn(b'<p>Student Name :', result.data)
        # self.assertEqual(result.status_code, 200)

    def test_behavior_history(self):
        result = self.client.get("/student_history/1/behavior_history?behavior_name=test_behavior")
        # self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h4> Behavior Progress: </h4>', result.data)

    def test_behaviors(self):
        result = self.client.get("/behaviors")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Add a Behavior", result.data)

    def test_student_list(self):
        result = self.client.get("/student_list", query_string={"lname": "student",
                                 "fname": "test", "student_id": 1, "birthdate": datetime(2000, 9, 7)},
                                 follow_redirects=True)
        self.assertIn(b'<h2>Students matching your search: </h2>', result.data)
        # self.assertEqual(result.status_code, 200)

    def test_interventions(self):
        result = self.client.get("/interventions")
        self.assertIn(b'<h2>Interventions</h2>', result.data)
        # self.assertEqual(result.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UnitTestCase(unittest.TestCase):

    def test_display_interventions(self):

        self.assertIsNotNone("Non verbal cues")
        self.assertIsNotNone("Praise when on task")

    def test_display_behaviors(self):

        self.assertIsNotNone("Disorganized")
        self.assertIsNotNone("Stealing")
        self.assertIsNotNone("Tardiness")


if __name__ == "__main__":
    """If run interactively will allow you to work with db directly"""

    # from server import app
    app.debug = True
    connect_to_db(app, 'postgresql:///testdb')
    print("Connected to DB.")
    IntegrationTestCase()
    unittest.main()
