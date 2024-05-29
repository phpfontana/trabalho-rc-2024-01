import unittest
from server.user import User
from server.errors import InvalidNicknameError


class TestCommandNick(unittest.TestCase):

    def setUp(self):
        self.user = User()

    def test_invalid_nickname(self):
        try:
            invalid_nick_by_initial_char = "_George"
            self.user.handle_command_nick(invalid_nick_by_initial_char)
        except InvalidNicknameError:
            pass
        try:
            invalid_nick_by_not_allowed_char = "Ringo@"
            self.user.handle_command_nick(invalid_nick_by_not_allowed_char)
        except InvalidNicknameError:
            pass
        try:
            invalid_nick_by_size = "Syd Barrett"
            self.user.handle_command_nick(invalid_nick_by_size)
        except InvalidNicknameError:
            pass

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
