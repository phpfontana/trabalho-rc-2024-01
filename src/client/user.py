from typing import List
from client.errors import InvalidNicknameError
from shared.utils import to_lowercase_bytes

class User:
    class UserConfig:
        def __init__(self, nickname_max_size):
            self.nickname_max_size = nickname_max_size

    class UserHistory:
        def __init__(self):
            self.nickname = []

    def __init__(self, nickname_max_size=9):
        self.nickname = bytearray()
        self.username = bytearray()
        self.registered = False
        self.channels: List = []
        self.default_channel:Channel = None
        self.configuration = self.UserConfig(nickname_max_size)
        self.history = self.UserHistory()

    def quit_all_channels(self):
        for channel in self.channels:
            channel.user_list.remove(self)

    def set_nickname(self, nickname: str): #TODO Think about when nickname is None
        if self.nickname is not None:
            if self.__is_valid_nickname(nickname):
                self.history.nickname.append(self.nickname)
                self.nickname = nickname
                self.normalized_nickname = nickname.lower()
            else:
                raise InvalidNicknameError(nickname)

    def __is_valid_nickname(self, nickname: str) -> bool:
        starts_with_letter = nickname[0].isalpha()
        on_size_limit = len(nickname) <= self.configuration.nickname_max_size
        only_alphanum_or_underline = self.__is_only_alphanum_or_underline(
            nickname[1:]
        )
        if starts_with_letter and on_size_limit and only_alphanum_or_underline:
            return True
        else:
            return False

    def is_registered(self) -> bool:
        self.registered = bool(self.nickname) and bool(self.username)
        return self.registered

    def is_first_nick(self) -> bool:
        return len(self.history.nickname) == 1

    def __is_only_alphanum_or_underline(
        self, nickname_without_first_letter: str
    ) -> bool:
        for char in nickname_without_first_letter:
            if not (char.isalnum() or char == "_"):
                return False
        return True