import logging
import socket
from _thread import start_new_thread
from collections import deque
from typing import List

from server.channel import Channel
from server.command_handler import CommandHandler
from server.connection import Connection
from server.errors import Errors
from server.message_to_send import MessageToSend
from server.processed_message import ProcessedMessage
from shared.logger import Logger


class Server:
    def __init__(
        self,
        motd=bytearray(
            b"Here we love overengeneering and unnecessary complexity leading to bad"
            b" code!"
        ),
        port=6667,
        enable_log=True,
        log_level=logging.INFO,
    ):
        self.port = port
        self.connections = deque()
        self.channels = []
        self.motd = motd
        self.command_handler = CommandHandler(self)
        self.logger = Logger(enabled=enable_log, level=log_level)

    def client_thread_loop(self, connection_socket: socket.socket):
        connection: Connection = Connection(connection_socket, self)
        self.connections.append(connection)
        while True:
            message: ProcessedMessage = connection.wait_for_message()
            self.logger.debug(b"Processing message: ", message)
            messages_to_send: List[MessageToSend] = self.message_handler(
                connection, message
            )
            if messages_to_send:
                for msg in messages_to_send:
                    self.logger.info(b"Sending message: ", msg.payload)
                    msg.send()

    def listen(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.bind(("", self.port))
        _socket.listen(4096)
        self.logger.info(f"Server Running on: {self.port}")
        while True:
            connection_socket, addr = _socket.accept()
            self.logger.info(f"Client Connected: {addr}")
            start_new_thread(self.client_thread_loop, (connection_socket,))

    def message_handler(self, connection: Connection, message: ProcessedMessage):
        command = message.command
        params = message.params
        match command:
            case b"NICK":
                try:
                    nickname = params[0]
                    messages_to_send = self.command_handler.nick(nickname, connection)
                    return messages_to_send
                except Errors.Nickname.InvalidNicknameError as e:
                    self.logger.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
                except Errors.Nickname.NicknameAlreadyInUseError as e:
                    self.logger.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
            case b"USER":
                try:
                    username = params[0]
                    message_to_send = self.command_handler.user(username, connection)
                    return message_to_send
                except Errors.Nickname.InvalidNicknameError as e:
                    self.logger.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
            case b"PRIVMSG":
                self.logger.debug("PRIVMSG command received")
                try:
                    channel_name = params[0]
                    user_msg = params[1][1:]
                    self.command_handler.privmsg(channel_name, user_msg, connection)
                except Errors.Join.InvalidChannelNameError as e:
                    self.logger.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
            case b"JOIN":
                try:
                    channel_name = params[0]
                    messages_to_send = self.command_handler.join(
                        channel_name, connection
                    )
                    return messages_to_send
                except Errors.Join.InvalidChannelNameError as e:
                    self.logger.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
            case b"NAMES":
                self.logger.debug("NAMES command received")
            case b"PART":
                self.logger.debug("PART command received")
                try:
                    channel_name = params[0]
                    messages_to_send = self.command_handler.part(
                        channel_name, connection
                    )
                    return messages_to_send
                except Errors.Part.NotOnChannelError as e:
                    self.logger.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
            case b"PING":
                try:
                    payload = params[0]
                    message_to_send = self.command_handler.ping(payload, connection)
                    return message_to_send
                except Exception as e:
                    print(e)
            case b"QUIT":
                self.logger.debug("QUIT command received")
            case _:
                self.logger.warning(f"Unknown command received: {command}")

    def is_nickname_free(self, nickname: bytearray) -> bool:
        for connection in self.connections:
            if connection.user.nickname == nickname:
                return False
        return True

    def find_channel_by_name(self, channel_name: bytearray) -> Channel | None:
        for channel in self.channels:
            if channel.name == channel_name:
                return channel
        return None

    def start(self):
        self.listen()
