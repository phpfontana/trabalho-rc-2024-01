from client.user import User
from client.client import Client

class MessageReceiver():
    def __init__(self, client:Client, user:User):
        self.client = client
        self.user = user
        self.message.raw = None
        self.message.main_command = None
        self.message.command_arguments = None

    def listen_server_messages(self):
        while(True):
            if self.client.connect:
                message = self.client.socket.recv(512)
                match message:
                    case bytes("PING"):
                        pass
                    case bytes(""):
                        pass

    def __parse_server_message(self, message):





