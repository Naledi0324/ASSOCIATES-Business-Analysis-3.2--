# Tests for Flask routes
import unittest
import json
from app import create_app, db
from flask_login import FlaskLoginClient

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_login(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_create_reminder(self):
        self.client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post('/reminders', json={
            'title': 'Test Reminder',
            'description': 'Test Description',
            'reminder_time': '2024-01-01T10:00:00'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_reminders(self):
        self.client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
        response = self.client.get('/reminders')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)  # Expecting a list of reminders

if __name__ == '__main__':
    unittest.main()
