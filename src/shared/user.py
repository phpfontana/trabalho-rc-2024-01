from logger import Logger

class User:
    class UserConfig:
        def __init__(self, nickname_max_size=9, debug_mode=False):
            self.nickname_max_size = nickname_max_size
            self.debug_mode = debug_mode

    class UserHistory:
        def __init__(self):
            self.nickname = []

    def __init__(self, nickname=None, nickname_max_size=9, debug_mode=False):
        self.nickname = None
        self.username = None
        self.configuration = self.UserConfig(nickname_max_size, debug_mode)
        self.history = self.UserHistory()
        self.logger = Logger(".client.log", debug_mode)

    def is_valid_nickname(self, nickname: str) -> bool:
        starts_with_letter = nickname.isalpha()
        on_size_limit = len(nickname) <= self.configuration.nickname_max_size
        only_alphanum_or_underline = self.__is_only_alphanum_or_underline(nickname[1:])

        if starts_with_letter and on_size_limit and only_alphanum_or_underline:
            return True
        else:
            return False

    def __is_only_alphanum_or_underline(self, nickname_without_first_letter: str) -> bool:
        for char in nickname_without_first_letter:
            if char.isalnum() or char == "_":
                pass
            else:
                self.logger.debug(f"Invalid character in nickname: {char}")
                return False
        return True
