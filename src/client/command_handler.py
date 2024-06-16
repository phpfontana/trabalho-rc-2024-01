from client.client import Client
from shared.user import User
from client.errors import InvalidNicknameError


class CommandHandler():
    def __init__(self, client:Client, user:User):
        self.client = client
        self.user = user
    
    def help(self):
        commands = {
            '/help': 'List all available commands with a brief description of each.',
            '/nick': 'Change the user nickname. Usage: /nick <new_nickname>',
            '/connect': 'Connect to the server. Usage: /connect <IP>',
            '/disconnect': 'Disconnect from the server. Usage: /disconnect :<reason>',
            '/quit': 'Exit the client. Usage: /quit :<reason>',
            '/join': 'Join a channel. Usage: /join #<channel>',
            '/leave': 'Leave a channel. Usage: /leave #<channel> <reason>',
            '/channel': 'Select a default channel. Usage: /channel #<channel>',
            '/list': 'List the users in a channel. Usage: /list #<channel>',
            '/msg': 'Send a message to a channel. Usage: /msg #<channel> <message>',
        }
        for command, description in commands.items():
            print(f"{command}: {description}")
   
    def motd(self, mtod):
        pass

    def nick(self, nickname:str):
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

    def __format_registration_msg(self):
        pass

    def __format_nick_change_msg(self):
        history = self.user.history
        return f'{history.nickname[len(history) - 1]} NICK {self.user.nickname}'
