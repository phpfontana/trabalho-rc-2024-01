class InvalidNicknameError(Exception):
    def __init__(self, nickname):
        self.error_code = 432
        self.nickname = nickname
        self.message = f"{self.error_code} * {self.nickname} :Erroneous Nickname"
        super().__init__(self.message)


class NicknameAlreadyInUseError(Exception):
    def __init__(self, nickname):
        self.error_code = 433
        self.nickname = nickname
        self.message = (
            f"{self.error_code} * {self.nickname} :Nickname is already in use"
        )
        super.__init__(self.message)
