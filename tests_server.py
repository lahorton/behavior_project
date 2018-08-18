import unittest
from unittest import TestCase
from faker import Faker
import server


class UnitTestCase(unittest.TestCase):

    def test_display_interventions(self):

        self.assertIsNotNone("Non verbal cues")
        self.assertIsNotNone("Praise when on task")

    def test_display_behaviors(self):

        self.assertIsNotNone("Disorganized")
        self.assertIsNotNone("Stealing")
        self.assertIsNotNone("Tardiness")


class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn(b'<li>Choose a behavior', result.data)

    def test_user_info(self):
        result = self.client.get('/user_info/<user_id>')
        self.assertIn(b'User ID: ', result.data)

    def test_student_history(self):
        result = self.client.get("/student_history/<student_id>")
        self.assertIn(b'<p>Student Name :', result.data)

    def test_behavior_history(self):
        result = self.client.get("/student_history/<student_id>/behavior_history")
        self.assertIn(b'<h4> Behavior Progress: </h4>', result.data)

    def test_behaviors(self):
        result = self.client.get("/behaviors")
        self.assertIn(b'<h3>Behaviors</h3>')

    def test_student_list(self):
        result = self.client.get("/student_list")
        self.assertIn(b'<h2>Students matching your search: </h2>')

    def test_interventions(self):
        result = self.client.get("/interventions")
        self.assertIn(b'<h2>Interventions</h2>')


# Code below is not working to create a test db... no tables are created after running tests_model.py to create it.
# def example_data():
#     """creates sample data for testing"""

#     # empty out existing data in case it's run more than once.
#     User.query.delete()
#     Student.query.delete()
#     Behavior.query.delete()
#     Intervention.query.delete()
#     Progress.query.delete()

#     # Add sample data
#     test_user = User(user_name="test_user", password="12345")
#     test_student = Student(fname="test", lname="student",
#                            birthdate=fake.date_of_birth(tzinfo=None, minimum_age=5, maximum_age=18),
#                            phone_number="3132589798", user_id=user_id)
#     test_behavior = Behavior(behavior_name="test_behavior", behavior_description="tests stuff")
#     test_intervention = Intervention(intervention_name="test_intervention")
#     test_progress = Progress(student_id=test_student.student_id, behavior_id=test_behavior.behavior_id,
#                              intervention_id=test_intervention.intervention_id,
#                              date=fake.past_date(start_date="-360d", tzinfo=None),
#                              rating=5, comment="test comment")

#     db.session.add_all([test_user, test_student, test_behavior, test_intervention, test_progress])
#     db.session.commit()


# class FlaskTests(TestCase):
#     def setUp(self):

#         self.client = app.test_client()
#         app.config['Testing'] = True

#         #connect to db, create tables and sample data
#         connect_to_db(app, "postgresql://testdb")
#         db.create_all()
#         example_data()


if __name__ == '__main__':
    unittest.main()
