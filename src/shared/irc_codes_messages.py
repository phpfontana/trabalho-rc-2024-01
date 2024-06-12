from random import randbytes
from server.server import Server
from shared.user import User


class IrcCodesMessages():
    class Nick():
        class RplWelcome():
            def __init__(self, user:User, server:Server):
                self.code = "001"
                self.msg = f"{self.code} {user.nickname} :Welcome to the Internet Relay Network {user.nickname}\r\rn" 

        class NickChange():
            def __init(self, user:User, server:server):
                self.msg = f":{user.history.nickname[-1]} NICK {user.nickname}\r\n"

        class ErrNicknameInUse():
            def __init__(self, user:User, server:Server):
                self.code = "433"
                self.msg = f"{self.code} * {user.nickname} :Nickname is already in use\r\n"

        class ErrErroneusNickname():
            def __init__(self, user:User, server:Server):
                self.code = "432"
                self.msg = f"{self.code} * {user.nickname} :Erroneous Nickname\r\n"

        def __init__(self, user:User, server:Server):
            self.RPL_WELCOME = self.RplWelcome(user,server)
            self.NICKCHANGE = self.NickChange(user,server)
            self.ERR_NICKNAMEINUSE = self.ErrErroneusNickname(user,server)
            self.ERR_ERRONEUSNICKNAME = self.ErrErroneusNickname(user, server)

   class Motd():
       class RplMotdStart():
           def __init(self, user:User, server:Server):
               self.code = "375"
               self.msg = f":server 375 {user.nickname} :- {server.ip} Message of the Day -\r\n"

       class RplMotd(self, user:User, server:Server):
               self.code = "372"
               self.msg = f":server 372 {user.nickname} :- {server.motd}\r\n"

       class RplEndOfMotd():
           def __init(self, user:User, server:Server):
               self.code = "376"
               self.msg = f":server 376 {user.nickname} :End of /MOTD command.\r\n"

       def __init__(self, user:User, server:Server):
            self.RPL_MOTDSTART = self.RplMotdStart(user,server)
            self.RPL_MOTD = self.RplMotd(user,server)
            self.RPL_ENDOFMOTD = self.RplEndOfMotd(user,server)

    class PingCommand():
        class Ping():
            def __init__(self, ping_command:PingCommand):
                self.ping_command = ping_command
            
            def msg(self):
                self.ping_command.payload = self.__generate_payload()
                return f"PING :{self.ping_command.payload}"

            def __generate_payload(self):
                return randbytes(4)

        class Pong():
            def __init__(self, ping_command:PingCommand):
                self.ping_command = ping_command

            def msg(self):
                return f"PONG :{self.ping_command.payload}"

        def __init__(self):
            self.payload = None
            self.PING = Ping(self)
            self.PONG = Pong(self)


    class Join 

    def __init__(self, user:User, server:Server):
        self.nick = self.Nick(user, server)
        self.__user = user
        self.__server = server
