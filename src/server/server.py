import socket
from _thread import start_new_thread
from collections import deque
from typing import List

from server.channel import Channel
from server.command_handler import CommandHandler
from server.connection import ClientConnection
from server.errors import Errors
from server.processed_message import ProcessedMessage
from shared.logger import Logger


class Server:
    def __init__(
        self,
        motd="Welcome to the Internet Relay Network",
        port=6667,
        debug_mode=False,
    ):
        self.port = port
        self.connections_list = deque()
        self.channels_list = deque()
        self.motd = motd
        self.command_handler = CommandHandler(self)
        self.debug_mode = debug_mode
        self.logger = Logger(".server.log", debug_mode)

    def client_thread_loop(self, connection_socket):
        try:
            connection = ClientConnection(connection_socket)
            self.connections_list.append(connection)
            message: ProcessedMessage = connection.wait_for_message()
            messages_to_send: List[self.MessageToSend] = self.message_handler(
                connection, message
            )
            for message in messages_to_send:
                message.send()
        except Exception as e:
            print(e)

    def listen(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.bind(("", self.port))
        _socket.listen(4096)

        while True:
            print(f"Servidor aceitando conexões na porta {self.port}...")
            connection_socket, addr = _socket.accept()
            start_new_thread(self.client_thread_loop, (connection_socket,))

    def message_handler(self, connection: ClientConnection, message: ProcessedMessage):
        command = message.command
        params = message.params
        match command:
            case b"NICK":
                try:
                    messages_to_send = self.command_handler.nick(*params, connection)
                    return messages_to_send
                except Errors.Nickname.InvalidNicknameError as e:
                    return e.message
                except Errors.Nickname.NicknameAlreadyInUseError as e:
                    return e.message
            case b"USER":
                try:
                    message_to_send = self.command_handler.user(*params, connection)
                    return message_to_send
                except Errors.Nickname.InvalidNicknameError as e:
                    return e.message
            case b"PRIVMSG":
                self.logger.debug("PRIVMSG command received")
            case b"JOIN":
                try:
                    messages_to_send = self.command_handler.join(*params, connection)
                    return messages_to_send
                except Exception as _:
                    print(_)
            case b"NAMES":
                self.logger.debug("NAMES command received")
            case b"PART":
                self.logger.debug("PART command received")
            case b"PING":
                try:
                    message_to_send = self.command_handler.ping(*params)
                    return message_to_send
                except Exception as e:
                    print(e)
            case b"QUIT":
                self.logger.debug("QUIT command received")
            case _:
                self.logger.warning(f"Unknown command received: {command}")

    def is_nickname_free(self, nickname: str) -> bool:
        for connection in self.connections_list:
            if connection.user.get_nickname() == nickname:
                return False
        return True

    def create_channel(self, channel_name: bytearray) -> Channel:
        new_channel = Channel(channel_name)
        self.channels_list.append(new_channel)
        return new_channel

    def find_channel_by_name(self, channel_name: bytearray) -> Channel | None:
        for channel in self.channels_list:
            if channel.name == channel_name:
                return channel
        return None


    def start(self):
        self.listen()
