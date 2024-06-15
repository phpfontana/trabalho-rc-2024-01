from socket import socket

from shared.utils import to_lowercase_bytes


class User:
    class UserConfig:
        def __init__(self, nickname_max_size):
            self.nickname_max_size = nickname_max_size

    class UserHistory:
        def __init__(self):
            self.nickname = []

    def __init__(self, connection_socket: socket, nickname_max_size=9):
        self.nickname = bytearray()
        self.normalized_nickname = bytearray()
        self.username = bytearray()
        self.normalized_username = bytearray()
        self.registered = False
        self.connection_socket = connection_socket
        self.configuration = self.UserConfig(nickname_max_size)
        self.history = self.UserHistory()

    def set_nickname(self, nickname: bytearray):
        if self.nickname is not None:
            self.history.nickname.append(self.nickname)
        self.nickname = nickname
        self.normalized_nickname = to_lowercase_bytes(nickname)

    def is_valid_nickname(self, nickname: bytearray) -> bool:
        try:
            nickname_str: str = nickname.decode()
        except UnicodeError as _:
            return False
        starts_with_letter = nickname_str[0].isalpha()
        on_size_limit = len(nickname_str) <= self.configuration.nickname_max_size
        only_alphanum_or_underline = self.__is_only_alphanum_or_underline(
            nickname_str[1:]
        )

        if starts_with_letter and on_size_limit and only_alphanum_or_underline:
            return True
        else:
            return False

    def is_first_nick(self) -> bool:
        return len(self.history.nickname) == 1

    def is_registered(self) -> bool:
        self.registered = bool(self.nickname) and bool(self.username)
        return self.registered

    def __is_only_alphanum_or_underline(
        self, nickname_without_first_letter: str
    ) -> bool:
        for char in nickname_without_first_letter:
            if not (char.isalnum() or char == "_"):
                return False
        return True
