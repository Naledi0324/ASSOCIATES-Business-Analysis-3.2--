 # Tests for database models
import unittest
from app import create_app, db
from app.models import User, Reminder, Feedback

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

    def test_reminder_creation(self):
        user = User(username='testuser2', email='test2@example.com')
        db.session.add(user)
        db.session.commit()

        reminder = Reminder(title='Test Reminder', description='Test Description', user_id=user.id)
        db.session.add(reminder)
        db.session.commit()
        self.assertEqual(reminder.title, 'Test Reminder')
        self.assertEqual(reminder.description, 'Test Description')

    def test_feedback_creation(self):
        user = User(username='testuser3', email='test3@example.com')
        db.session.add(user)
        db.session.commit()

        feedback = Feedback(content='This is a test feedback', user_id=user.id)
        db.session.add(feedback)
        db.session.commit()
        self.assertEqual(feedback.content, 'This is a test feedback')

if __name__ == '__main__':
    unittest.main()
