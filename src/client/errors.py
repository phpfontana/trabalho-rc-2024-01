class InvalidNicknameError(Exception):
    def __init__(self, nickname:str):
        self.nickname = nickname
        self.message = f"Choose another nickname '{nickname}' is invalid"
        super().__init__(self.message)

class CommandShouldStartWithBackslashError(Exception):
    def __init__(self, user_input):
        self.user_input = user_input
        self.message = f"Every command should start with backslash '\\' char!\n Your command: {user_input}"
        super().__init__(self.message)

