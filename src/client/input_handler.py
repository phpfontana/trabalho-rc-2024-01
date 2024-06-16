from client.client import Client
from client.command_handler import CommandHandler
from client.user import User
from client.errors import CommandOnlyUsableConnectedError


class InputHandler():
    def __init__(self, client:Client, user:User):
        self.client = client
        self.user = user
        self.command_handler = CommandHandler()

    def listen_command_input(self):
        while(True):
            try:
                user_input = self.__safe_read_input()
                command, params = self.__separate_command_params(user_input)
                match command:
                    case "nick":
                        try:
                            nick = params[0]
                            self.command_handler.nick(nick)
                        except IndexError:
                            print("Missing nick param!")
                    case "connect":
                        pass
                    case "disconnect":
                        pass
                    case "quit":
                        pass
                    case "join":
                        pass
                    case "leave":
                        pass
                    case "part":
                        pass
                    case "channel":
                        pass
                    case "list":
                        pass
                    case "msg":
                        pass
                    case "help":
                        pass
                    case _:
                        pass
            except CommandOnlyUsableConnectedError as e:
                print(e.msg)
    
    def __separate_command_params(self, user_input):
        if user_input[0] != '\\':
            return self.__ignore_or_generate_msg_to_default_channel()
        input_without_backslash = user_input[1:]
        command, params = input_without_backslash.split(" ",1)
        return (command, params)


    def __ignore_or_generate_msg_to_default_channel(self, user_input):
       if self.user.default_channel:
           return ("msg", [self.user.default_channel.name, user_input])
       else:
           return ("", [])


    def __safe_read_input(self):
        while True:
            try:
                user_input = input()
                return user_input
            except UnicodeError:
                print("The input should be valid text (utf-8 encoding)")

    def __check_params(self, number_of_params):
        pass
