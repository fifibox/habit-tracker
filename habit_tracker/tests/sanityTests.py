import unittest
from app.models import User

class TestSanity(unittest.TestCase):
    def test_user_model(self):
        self.assertIsNotNone(User)