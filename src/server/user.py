from errors import InvalidNicknameError

from utils.logger import Logger


class User:
    class UserConfig:
        def __init__(self, nickname_max_size=9, debug_mode=False):
            self.nickname_max_size = nickname_max_size
            self.debug_mode = debug_mode

    def __init__(
        self,
        nickname_max_size=9,
        debug_mode=False,
    ):
        self.nickname = None
        self.username = None
        self.configuration = self.UserConfig(nickname_max_size, debug_mode)

        self.logger = Logger(".server.log", debug_mode)

    def handle_command_nick(self, nickname: str) -> str:
        if self.is_valid_nickname(nickname):
            self.nickname = nickname
            success_nickname_message = (
                f"001 {
                    self.nickname} :Welcome to the Internet"
                f" Relay Network {self.nickname}\r\n"
            )
            self.logger.info(f"Nickname set: {nickname}")
            return success_nickname_message
        else:
            self.logger.warning(f"Invalid nickname set attempt: {nickname}")
            raise InvalidNicknameError(nickname)

    def handle_command_user(self, username: str) -> bool:
        self.username = username
        self.logger.info(f"Username set: {self.username}")
        return True

    def handle_command_motd(self, message_of_the_day, host) -> str:
        message_of_the_day = (
            f":server 375 {self.nickname} :- {host} Message of the day\r\n"
            f":server 372 {self.nickname} :- {message_of_the_day}\r\n"
            f":server 376 {self.nickname} :End of /MOTD command\r\n"
        )
        self.logger.debug(f"MOTD created - {message_of_the_day}")
        return message_of_the_day

    def handle_command_ping(self, ping_payload):
        self.send_data(f"PONG :{ping_payload}\r\n")
        self.logger.debug(f"PONG sent to {self.nickname}")

    def is_registered(self) -> bool:
        registered = self.nickname and self.username
        self.logger.debug(f"Is registered: {registered}")
        return registered

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
                self.logger.debug(f"Invalid character in nickname: {char}")
                return False
        return True
