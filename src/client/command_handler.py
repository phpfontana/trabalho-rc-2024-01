from client.client import Client
from shared.user import User
import socket
from client.errors import InvalidNicknameError
from client.errors import SendDataToServerError


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
    
    def connect(self, addr):
        retry = 3
        while (retry):
            try:
                self.client.connect((addr, self.port))
                self.__send_to_server(self.__format_registration_msg())
            except SendDataToServerError as e:
                print(e.msg)
            except socket.error as e:
                print("Erro tentar se conectar ao servidor!")
                print(e)
                retry -= 1
                print(f"Retry {retry}")

    def nick(self, nickname:str):
        try:
            self.user.set_nickname(nickname)
            if self.client.connected and self.user.is_registered():
                self.__send_to_server(self.__format_nick_change_msg())
            else:
                print("You are not connected to any server!")
                print(f"Nick setted locally to {self.user.nickname}!")
        except InvalidNicknameError as e:
            print(e.msg)
            
    def __format_nick_msg(self):
        return f'NICK :{self.user.nick}\r\n'.encode()

    def __format_user_msg(self):
        return f"USER {self.user.nick}\r\n".encode()

    def __format_registration_msg(self):
        return self.__format_nick_msg() + self.__format_user_msg()

    def __format_nick_change_msg(self):
        history = self.user.history
        return f'{history.nickname[len(history) - 1]} NICK {self.user.nickname}'.encode()

    def __send_to_server(self,msg:bytearray):
        try:
            self.client.server_socket.sendall(msg)
        except socket.error as e:
            raise SendDataToServerError(e, msg)
