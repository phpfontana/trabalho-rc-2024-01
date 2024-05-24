class User:

    class Configuration:

        def __init__(self):
            self.nickname_max_size = 9

    def __init__(self):
        self.nickname = None
        self.username = None
        self.configuration = self.Configuration()

    def handle_command_nick(self, nickname: str) -> bool:
        if self.is_valid_nickname(nickname):
            self.nickname = nickname
            return True
        else:
            return False

    def handle_command_user(self, username: str) -> bool:
        if self.is_registered():
            return False
        else:
            self.username = username
            return True

    def is_registered(self) -> bool:
        if self.nickname and self.username:
            return True
        else:
            return False

    def is_valid_nickname(self, nickname: str) -> bool:
        starts_with_letter = nickname.isalpha()
        on_size_limit = len(nickname) <= self.configuration.nickname_max_size
        only_alphanum_or_underline = self.is_only_alphanum_or_underline(nickname[1:])

        if starts_with_letter and on_size_limit and only_alphanum_or_underline:
            return True
        else:
            return False

    def is_only_alphanum_or_underline(self, nickname_without_first_letter: str) -> bool:
        for char in nickname_without_first_letter:
            if char.isalnum() or char == "_":
                pass
            else:
                return False
        return True
