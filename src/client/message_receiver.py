from client.user import User
from client.client import Client
from client.processed_message import ProcessedMessage
from client.errors import Errors
import logging

class MessageReceiver():
    def __init__(self, client:Client, user:User, logger):
        self.client = client
        self.user = user
        self.buffer = bytearray()
        self.logger = logger


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


    def __handle_server_response(self, processed_message):
        message = self.message
        command_or_code = self.command_or_code

        match command_or_code:
            case b"NICK":
                return b"COMMAND: NICK"
            case b"PING":
                return b"COMMAND: PING"
            case b"PONG":
                return b"COMMAND: PONG"
            case b"JOIN":
                return b"COMMAND: JOIN"
            case b"PART":
                return b"COMMAND: PART"
            case b"QUIT":
                return b"COMMAND: QUIT"
            case b"PRIVMSG":
                return b"COMMAND: PRIVMSG"
            case b"NAMES":
                return b"COMMAND: NAMES"
            case b"001":
                self.handle_001(message)
            case b"433":
                return b"CODE: 433"
            case b"432":
                return b"CODE: 432"
            case b"375":
                return b"CODE: 375"
            case b"372":
                return b"CODE: 372"
            case b"376":
                return b"CODE: 376"
            case b"403":
                return b"CODE: 403"
            case b"353":
                return b"CODE: 353"
            case b"366":
                return b"CODE: 366"
            case b"442":
                return b"CODE: 442"
            case _:
                return None


    def handle_001(self, message: bytearray):
        self.client.user.registered = True
        welcome_msg = message.split(b" ")[2]
        print(welcome_msg)

    def listen_server_messages(self):
        while(True):
            processed_message = self.wait_for_message()
            self.__handle_server_response(processed_message)
