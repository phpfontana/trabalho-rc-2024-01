class InvalidNicknameError(Exception):
    def __init__(self, nickname: str):
        self.nickname = nickname
        self.msg = f"Choose another nickname {nickname} is invalid"
        super().__init__(self.msg)

class CommandShouldStartWithBackslashError(Exception):
    def __init__(self, user_input):
        self.user_input = user_input
        self.msg = f"Every command should start with backslash '\\' char!\n Your command: {user_input}"
        super().__init__(self.msg)

