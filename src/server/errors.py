from shared.irc_codes import IrcCodes

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
                    f"{self.error_code} * {self.nickname} :Nickname is already in use\r\n"
                ).encode()
                super().__init__(self.message)
    class Username:
        class UsernameChangeAttempt(Exception):
            pass

    class Join:
        class InvalidChannelNameError(Exception):
            def __init__(self, nickname:str,host:str, channel_name:bytearray):
                self.error_code = IrcCodes.Join.ERR_NOSUCHCHANNEL
                self.channel_name = channel_name
                self.__first_part_of_message = (f":{self.host} {self.error_code} {nickname} ")
                self.__final_part_of_message = " :No such channel"
                self.message = self.__first_part_of_message.encode() + channel_name + self.__final_part_of_message.encode()


    class NoEndMessageCharsFoundError(Exception):
        def __init__(self):
            pass
