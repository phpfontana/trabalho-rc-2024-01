from client.user import User
from client.processed_message import ProcessedMessage
from datetime import datetime
from client.errors import InvalidChannelNameError
from client.errors import Errors
import logging
from client.channel import Channel

class MessageReceiver():
    def __init__(self, client, user:User, logger, close=False):
        self.client = client
        self.user = user
        self.close = close
        self.buffer = bytearray()
        self.logger = logger


    def wait_for_message(self) -> ProcessedMessage:
        data_chunk = bytearray()
        if not self.buffer:
            data_chunk = self.client.server_socket.recv(512)
            self.logger.log_colored.in_(logging.INFO, data_chunk)
            if data_chunk == b"":
                raise Errors.Connection.ConnectionClosedByPeer(self)
        self.buffer.extend(data_chunk)
        processed_message = ProcessedMessage(self.buffer, self.logger)
        self.buffer = processed_message.remaining_buffer
        return processed_message


    def __handle_server_response(self, processed_message):
        message = processed_message.message
        command_or_code = processed_message.command_or_code
        match command_or_code:
            case b"NICK":
                self.handle_code_nick(message)
            case b"PING":
                self.handle_ping(message)
            case b"PONG":
                return b"COMMAND: PONG"
            case b"JOIN":
                self.handle_code_join(message)
            case b"PART":
                self.handle_part(message)
            case b"QUIT":
                self.handle_quit(message)
            case b"PRIVMSG":
                self.handle_privmsg(message)
            case b"001":
                self.logger.log.debug(message)
                self.handle_001(message)
            case b"433":
                self.handle_433(message)
            case b"432":
                self.handle_432(message)
            case b"375" | b"372" | b"376":
                self.handle_375_372_376(message)
            case b"403":
                self.handle_code_403(message)
            case b"353":
                self.handle_code_353(message)
            case b"366":
                self.handle_code_366(message)
            case b"442":
                self.handle_442(message)
            case _:
                return None

    def handle_ping(self, message):
        self.client.server_socket.sendall("PONG " + message.split(b" ")[1])

    def handle_privmsg(self, message):
        splited_priv = message.split(b" ",3)
        nickname = splited_priv[0][1:].decode()
        channel_name = splited_priv[2][1:].decode()
        msg = splited_priv[3].decode()
        self.print_msg(nickname, channel_name, msg)

    def handle_quit(self, message):
        print(message.decode())
    
    def handle_part(self, message):
        print(message.decode())

    def handle_375_372_376(self, message):
        self.logger.log.debug(message)
        print(message.split(b" ",3)[3].decode())

    def handle_442(self, message):
        print(message.split(b" ",3)[3].decode())
    
    def handle_432(self, message: bytearray):
        nick_in_use_msg = message.split(b" ",2)[2].decode()
        print(nick_in_use_msg)

    def handle_433(self, message: bytearray):
        nick_in_use_msg = message.split(b" ",2)[2].decode()
        print(nick_in_use_msg)

    def handle_001(self, message: bytearray):
        self.client.user.registered = True
        self.client.connected = True
        welcome_msg = message.split(b" ",2)[2].decode()
        print(welcome_msg)

    def handle_code_nick(self, message: bytearray):
        nick = message.split(b" ")[2]
        self.client.user.set_nickname(nick)
        print(message.decode())

    def handle_code_join(self, message: bytearray):
        try:
            splited_join = message.split(b" ")
            channel_name = splited_join[2][1:]
            self.logger.log.debug(channel_name)
            new_channel = Channel(channel_name.decode())
            self.client.user.join_channel(new_channel)
            print(message.decode())
        except InvalidChannelNameError as e:
            print(e.msg)
            
    def handle_code_403(self, message: bytearray):
        self.logger.log.debug(message)
        message = message.split(b" ", 3)[3]
        self.logger.log.debug(message)
        print(message.decode())

    def handle_code_353(self, message: bytearray):
        message = message.split(b" ", 4)[4]
        print(message.decode())

    def handle_code_366(self, message: bytearray):
        message = message.split(b" ", 3)[3]
        print(message.decode())

    def print_msg(self, nickname: str, channel_name: str, msg: str):
        hour_minute = datetime.now().strftime("%H:%M")
        print(f"{hour_minute} [{channel_name}] <{nickname}> {msg}\r\n")

    def listen_server_messages(self):
        while(not self.close):
            try:
                processed_message = self.wait_for_message()
            except Errors.Connection.ConnectionClosedByPeer:
                self.close = True
            self.logger.log.debug(processed_message.message)
            self.logger.log.debug(processed_message.command_or_code)
            self.__handle_server_response(processed_message)
