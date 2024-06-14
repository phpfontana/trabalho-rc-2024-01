from server.errors import InvalidNicknameError
from shared.utils import to_lowercase_bytes
from socket import socket


class User:
    class UserConfig:
        def __init__(self, nickname_max_size=9, debug_mode=False):
            self.nickname_max_size = nickname_max_size
            self.debug_mode = debug_mode

    class UserHistory:
        def __init__(self):
            self.nickname = []

    def __init__(self, connection_socket:socket, nickname_max_size=9, debug_mode=False):
        self.nickname = None
        self.normalized_nickname = None
        self.username = None
        self.normalized_username = None
        self.registered = False
        self.connection_socket = connection_socket
        self.configuration = self.UserConfig(nickname_max_size, debug_mode)
        self.history = self.UserHistory()

    def set_nickname(self, nickname: bytearray):
        if self.nickname is not None:
            self.history.nickname.append(self.nickname)
        self.nickname = nickname
        self.normalized_nickname = to_lowercase_bytes(nickname)

    def is_valid_nickname(self, nickname: bytearray) -> bool:
        try:
            nickname = nickname.decode()
        except UnicodeError as _:
            return False
        starts_with_letter = nickname.isalpha()
        on_size_limit = len(nickname) <= self.configuration.nickname_max_size
        only_alphanum_or_underline = self.__is_only_alphanum_or_underline(nickname[1:])

        if starts_with_letter and on_size_limit and only_alphanum_or_underline:
            return True
        else:
            return False

    def __is_only_alphanum_or_underline(
        self, nickname_without_first_letter: str
    ) -> bool:
        for char in nickname_without_first_letter:
            if not (char.isalnum()) or (char != "_"):
                return False
        return True
