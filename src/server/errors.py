from shared.irc_codes import IrcCodes
from shared.utils import format_byte_message


class Errors:
    class Registration:
        class UserNotRegisteredError(Exception):
            def __init(self):
                pass

    class Nickname:
        class InvalidNicknameError(Exception):
            def __init__(self, nickname):
                self.error_code = IrcCodes.Nick.ERR_NICKNAMEINUSE
                self.nickname = nickname
                self.message = (
                    f"{self.error_code} * {self.nickname} :Erroneous Nickname\r\n"
                ).encode()
                super().__init__(self.message)

        class NicknameAlreadyInUseError(Exception):
            def __init__(self, nickname):
                self.error_code = IrcCodes.Nick.ERR_ERRONEUSNICKNAME
                self.nickname = nickname
                self.message = (
                    f"{self.error_code} * {self.nickname} :Nickname is already in"
                    " use\r\n"
                ).encode()
                super().__init__(self.message)

    class Username:
        class UsernameChangeAttempt(Exception):
            pass

    class Join:
        class InvalidChannelNameError(Exception):
            def __init__(
                self, nickname: bytearray, host: bytearray, channel_name: bytearray
            ):
                self.error_code = IrcCodes.Join.ERR_NOSUCHCHANNEL
                self.channel_name = channel_name
                self.nickname = nickname
                self.host = host
                self.message = format_byte_message(
                    b":" + host,
                    self.error_code,
                    nickname,
                    channel_name,
                    b" :No such channel",
                )
                super().__init__(self.message)

    class NoEndMessageCharsFoundError(Exception):
        def __init__(self):
            pass
