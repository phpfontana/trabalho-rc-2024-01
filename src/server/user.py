from utils.logger import Logger


class User:
    class Configuration:
        def __init__(self, debug_mode=False):
            self.nickname_max_size = 9
            self.debug_mode = debug_mode

    def __init__(self, debug_mode=False):
        self.nickname = None
        self.username = None
        self.configuration = self.Configuration()

        if debug_mode:
            self.logger = Logger(".server.log")

    def handle_command_nick(self, nickname: str) -> bool:
        if self.is_valid_nickname(nickname):
            self.nickname = nickname
            if self.configuration.debug_mode:
                self.logger.info(f"Nickname set: {nickname}")
            return True
        else:
            if self.configuration.debug_mode:
                self.logger.warning(f"Invalid nickname set attempt: {nickname}")
            return False

    def handle_command_user(self, username: str) -> bool:
        if self.is_registered():
            if self.configuration.debug_mode:
                self.logger.warning("User already registered")
            return False
        else:
            if self.configuration.debug_mode:
                self.logger.info(f"Username set: {self.username}")
            self.username = username
            return True

    def handle_command_motd(self, motd):
        motd_message = (
            f":server 375 {self.nickname} :- Message of the day\r\n:server 372"
            f" {
                self.nickname} :- {motd}\r\n:server 376"
            f" {self.nickname} :End of MOTD command\r\n"
        )
        self.send_data(motd_message)
        if self.configuration.debug_mode:
            self.logger.debug(f"MOTD sent to {self.nickname}")

    def handle_command_ping(self, command_params):
        self.send_data(f"PONG :{command_params[0]}\r\n")
        if self.configuration.debug_mode:
            self.logger.debug(f"PONG sent to {self.nickname}")

    def is_registered(self) -> bool:
        registered = self.nickname and self.username
        if self.configuration.debug_mode:
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
                if self.configuration.debug_mode:
                    self.logger.debug(f"Invalid character in nickname: {char}")
                return False
        return True
