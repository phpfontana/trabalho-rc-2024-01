class InvalidNicknameError(Exception):
    def __init__(self, nickname: str):
        self.nickname = nickname
        self.msg = f"Choose another nickname {nickname} is invalid"
        super().__init__(self.msg)


class InvalidChannelNameError(Exception):
    def __init__(self, channel_name):
        self.channel_name = channel_name 
        self.msg = f"{channel_name} is a invalid channel name!"
        super().__init__(self.msg)

class CommandOnlyUsableConnectedError(Exception):
    def __init__(self, command_name:str):
        self.command_name = command_name
        self.msg = f"{command_name} can only be used when connected to a server!"

class SendDataToServerError(Exception):
    def __init__(self, socket_e, data:bytearray):
        self.data = data
        self.socket_e = socket_e
        self.msg = f"Error trying to send data to the server!\nError: {socket_e} Data: {data}"

class CommandShouldStartWithBackslashError(Exception):
    def __init__(self, user_input):
        self.user_input = user_input
        self.msg = f"Every command should start with backslash '\\' char!\n Your command: {user_input}"
        super().__init__(self.msg)

