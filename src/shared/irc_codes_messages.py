from server.server import Server
from shared.user import User
class IrcCodesMessages():
    class Nick():
        class RplWelcome():
            def __init__(self, user:User, server:Server):
                self.code = "001"
                self.msg = f"{self.code} {user.nickname} :Welcome to the Internet Relay Network {user.nickname}" 

        class NickChange():
            def __init(self, user:User, server:server):
                self.msg = f":{user.history.nickname[-1]} NICK {user.nickname}"

        class ErrNicknameInUse():
            def __init__(self, user:User, server:Server):
                self.code = "433"
                self.msg = f"{self.code} * {user.nickname} :Nickname is already in use"

        class ErrErroneusNickname():
            def __init__(self, user:User, server:Server):
                self.code = "432"
                self.msg = f"{self.code} * {user.nickname} :Erroneous Nickname"

        def __init__(self, user:User, server:Server):
            self.RPL_WELCOME = self.RplWelcome(user,server)
            self.ERR_NICKNAMEINUSE = self.ErrErroneusNickname(user,server)
            self.ERR_ERRONEUSNICKNAME = self.ErrErroneusNickname(user, server)

   class  


    def __init__(self, user:User, server:Server):
        self.nick = self.Nick(user, server)
        self.__user = user
        self.__server = server
