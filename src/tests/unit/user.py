import unittest
from server.user import User


class TestCommandUser(unittest.TestCase):

    def setUp(self):
        self.user = User()

    def test_set_username(self):
        username = "John"
        self.user.handle_command_user(username)

        self.assertEqual(self.user.username, username)

    def test_change_username(self):
        original_username = "John"
        self.user.handle_command_user(original_username)
        new_username = "Paul"
        self.user.handle_command_user(new_username)

        self.assertEqual(self.user.username, original_username)


if __name__ == "__main__":
    unittest.main()
