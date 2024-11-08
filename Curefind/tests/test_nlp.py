# Tests for NLP functionalities
import unittest
from app.other_features.chatbot import send_reminder  

class TestNLP(unittest.TestCase):

    def test_greeting_response(self):
        # Test that the chatbot responds correctly to a greeting
        response = send_reminder("Hello")
        self.assertIn("Hello", response, "Chatbot did not respond correctly to a greeting.")

    def test_medication_reminder(self):
        # Test chatbot response for a medication reminder query
        response = send_reminder("When should I take my medication?")
        self.assertTrue(any(phrase in response for phrase in ["take", "medication", "reminder"]), 
                        "Chatbot did not provide a suitable reminder response.")

    def test_unknown_query(self):
        # Test chatbot's handling of an unknown query
        response = send_reminder("What is the weather?")
        self.assertIn("I'm not sure", response, "Chatbot did not handle an unknown query appropriately.")

    def test_empty_input(self):
        # Test chatbot's response to an empty input
        response = send_reminder("")
        self.assertIn("Can you please ask something?", response, "Chatbot should prompt the user on empty input.")

if __name__ == '__main__':
    unittest.main()
