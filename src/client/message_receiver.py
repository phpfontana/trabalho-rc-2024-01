from client.user import User
from client.client import Client

class MessageReceiver():
    def __init__(self, client:Client, user:User, logger):
        self.client = client
        self.user = user
        self.buffer = bytearray()
        self.logger = logger
        self.message.raw = None
        self.message.main_command = None
        self.message.command_arguments = None


    def wait_for_message(self) -> ProcessedMessage:
        try:
            if not self.buffer:
                data_chunk = self.client.server_socket.recv(512)
                self.logger.log_colored.in_(logging.INFO, data_chunk)
                if data_chunk == b"":
                    raise Errors.Connection.ConnectionClosedByPeer(self)
            self.buffer.extend(data_chunk)
            processed_message = ProcessedMessage(self.buffer, self.__server.logger)
            self.buffer = processed_message.remaining_buffer
            self.message_history.append(processed_message)
            return processed_message
        except Errors.NoEndMessageCharsFoundError:
            return False

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
