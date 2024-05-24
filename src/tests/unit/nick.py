import unittest
from server.user import User


class TestCommandNick(unittest.TestCase):

    def setUp(self):
        self.user = User()

    def test_invalid_nickname(self):
        invalid_nick_by_initial_char = "_George"
        self.user.handle_command_nick(invalid_nick_by_initial_char)
        invalid_nick_by_not_allowed_char = "Ringo@"
        self.user.handle_command_nick(invalid_nick_by_not_allowed_char)
        invalid_nick_by_size = "Syd Barrett"
        self.user.handle_command_nick(invalid_nick_by_size)

        self.assertIsNone(self.user.nickname)

    def test_set_nickname(self):
        nickname = "John"
        self.user.handle_command_nick(nickname)

        self.assertEqual(self.user.nickname, nickname)

    def test_nickname_change(self):
        original_nickname = "John"
        self.user.handle_command_nick(original_nickname)
        new_nickname = "Paul"
        self.user.handle_command_nick(new_nickname)

        self.assertEqual(self.user.nickname, new_nickname)


if __name__ == "__main__":
    unittest.main()
