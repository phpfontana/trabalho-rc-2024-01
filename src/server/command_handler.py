from utils.logger import Logger

from server.errors import InvalidNicknameError
from shared.users import User


class CommandHandler:
    def __init__(
        self,
        debug_mode=False,
    ):
        self.user = User
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
