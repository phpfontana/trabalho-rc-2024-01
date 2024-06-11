from client.errors import CommandShouldStartWithBackslashError
from client.command_handler import CommandHandler
from shared.user import User
from client.client import Client

class InputHandler():
    def __init__(self, client:Client, user:User):
        self.client = client
        self.user = user

    def listen_command_input(self):
        command_handler = CommandHandler()
        while(True):
            user_input = input()
            command, params = self.__separate_command_params(user_input)
            match command:
                case "nick":
                    nick = params[0]
                    command_handler.handle_nick(nick)
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
    
    def __separate_command_params(self, user_input):
        if user_input[0] != '\\':
            raise CommandShouldStartWithBackslashError(user_input)
        input_without_backslash = user_input[1:]
        command, params = input_without_backslash.split(" ",1)
        return (command, params)

