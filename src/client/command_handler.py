from client.client import Client
from shared.user import User
from client.errors import InvalidNicknameError


class CommandHandler():
    def __init__(self, client:Client, user:User):
        self.client = client
        self.user = user
   
    def handle_command_motd(self, mtod):


    def handle_nick(self, nickname:str):
        if self.user.is_valid_nickname(nickname):
            self.user.nickname = nickname
            if self.client.connected:
                message = self.format_nick_request()
                self.client.socket.send(message)
        else:
            raise InvalidNicknameError(nickname)

    def __format_user_request(self):
        return f"USER {self.user.nick} 0 = :realname"

    def __format_nick_request(self):
        return f'NICK :{self.user.nick}\r\n'
