from client.client import Client
from shared.user import User
from client.errors import InvalidNicknameError


class CommandHandler():
    def __init__(self, client:Client, user:User):
        self.client = client
        self.user = user
   
    def handle_command_motd(self, mtod):
        pass

    def handle_nick(self, nickname:str):
        try:
            self.user.set_nickname(nickname)
            if self.client.connected:
                if self.user.is_registered():
                    if self.user.is_first_nick():
                        pass
                    else:
                        pass
                message = self.__format_nick_msg()
                self.client.socket.send(message)
            else:
                pass #local nick change
                
        except InvalidNicknameError as e:
            print(e.m)
            

    def __format_nick_msg(self):
        return f'NICK :{self.user.nick}\r\n'

    def __format_user_msg(self):
        return f"USER {self.user.nick}\r\n"

    def __format_nick_change_msg(self):
        history = self.user.history
        return f'{history.nickname[len(history) - 1]} NICK {self.user.nickname}'
