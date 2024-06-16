from client.client import Client
from client.command_handler import CommandHandler
from client.errors import CommandOnlyUsableConnectedError
from client.user import User


class InputHandler:
    def __init__(self, client: Client, user: User):
        self.client = client
        self.user = user
        self.command_handler = CommandHandler()

    def listen_command_input(self):
        while True:
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
                        try:
                            ip = params[0]
                            self.command_handler.connect(ip)
                        except IndexError:
                            print("Missing ip param!")
                    case "disconnect":
                        try:
                            reason = params[0]
                            self.command_handler.disconnect(reason)
                        except IndexError:
                            self.command_handler.disconnect()
                    case "quit":
                        try:
                            reason = params[0]
                            self.command_handler.quit(reason)
                        except IndexError:
                            self.command_handler.quit()
                    case "join":
                        try:
                            channel_name = params[0]
                            self.command_handler.join(channel_name)
                        except IndexError:
                            print("Missing channel_name param!")
                    case "leave" | "part":
                        channel_name = None
                        try:
                            channel_name = params[0]
                        except IndexError:
                            print("Missing channel_name param!")
                            return
                        try:
                            reason = params[1]
                            self.command_handler.leave(channel_name, params)
                        except IndexError:
                            self.command_handler.leave(channel_name)
                    case "channel":
                        try:
                            channel_name = params[0]
                            self.command_handler.channel(channel_name)
                        except IndexError:
                            self.command_handler.channel(channel_name)
                    case "list":
                        try:
                            channel_name = params[0]
                            self.command_handler.list(channel_name)
                        except IndexError:
                            self.command_handler.list()
                    case "msg":
                        channel_name = None
                        try:
                            channel_name = params[0]
                        except IndexError:
                            print("Missing msg param!")
                            return
                        try:
                            msg = params[1]
                            self.command_handler.msg(msg, channel_name)
                        except IndexError:
                            msg = params[0]
                            self.command_handler.msg(msg)
                    case "help":
                        self.command_handler.help()
                    case _:
                        self.command_handler.help()
                        print("Invalid command!")

            except CommandOnlyUsableConnectedError as e:
                print(e.msg)

    def __separate_command_params(self, user_input):
        if user_input[0] != "\\":
            return self.__ignore_or_generate_msg_to_default_channel()
        input_without_backslash = user_input[1:]
        command, params = input_without_backslash.split(" ", 1)
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
