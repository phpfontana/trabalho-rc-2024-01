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
from server.user import User
from shared.utils import to_lowercase_bytes


class Server:
    def __init__(
        self,
        motd=bytearray(
            b"Here we love overengeneering and unnecessary complexity leading to bad"
            b" code!"
        ),
        port=6667,
        enable_log=True,
        log_level=logging.DEBUG,
    ):
        self.port = port
        self.connections = deque()
        self.channels = []
        self.motd = motd
        self.command_handler = CommandHandler(self)
        self.logger = Logger(enabled=enable_log, level=log_level)

    def client_thread_loop(self, connection: Connection):
        while not connection.is_closed:
            try:
                message: ProcessedMessage = connection.wait_for_message()
                self.logger.log.debug(b"Processing message: " + message.message)
                messages_to_send: List[MessageToSend] = self.message_handler(
                    connection, message
                )
                if messages_to_send:
                    for msg in messages_to_send:
                        self.logger.log_colored.out(logging.INFO, self.__format_out_log(msg))
                        msg.send()
            except Errors.Connection.ConnectionClosedByPeer as e:
                self.logger.log_colored.out(logging.INFO, e.log_msg)
                self.disconnect_user(connection.user, connection)
                break

    def listen(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.bind(("", self.port))
        _socket.listen(4096)
        self.logger.log.info(f"Server Running on: {self.port}")
        while True:
            connection_socket, addr = _socket.accept()
            self.logger.log_colored.in_(logging.INFO, f"Client Connected: {addr}")
            connection = Connection(connection_socket, addr, self)
            self.connections.append(connection)
            start_new_thread(self.client_thread_loop, (connection,))

    def message_handler(self, connection: Connection, message: ProcessedMessage):
        command = message.command
        params = message.params
        self.logger.log.debug(command)
        self.logger.log.debug(params)
        match command:
            case b"NICK":
                try:
                    nickname = params[0]
                    return self.command_handler.nick(nickname, connection)
                except Errors.Nickname.InvalidNicknameError as e:
                    self.logger.log.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
                except Errors.Nickname.NicknameAlreadyInUseError as e:
                    self.logger.log.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
                except IndexError:
                    self.logger.log.error(command + b" Missing parameters")
            case b"USER":
                try:
                    username = params[0]
                    return self.command_handler.user(username, connection)
                except Errors.Nickname.InvalidNicknameError as e:
                    self.logger.log.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
                except IndexError:
                    self.logger.log.error(command + b" Missing parameters")
            case b"PRIVMSG":
                try:
                    channel_name = params[0]
                    user_msg = params[1]
                    messages_to_send = self.command_handler.privmsg(
                        channel_name, user_msg, connection
                    )
                    return messages_to_send
                except Errors.Join.InvalidChannelNameError as e:
                    self.logger.log.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
                except IndexError:
                    self.logger.log.error(command + b" Missing parameters")
            case b"JOIN":
                try:
                    channel_name = params[0]
                    return self.command_handler.join(channel_name, connection)
                except Errors.Join.InvalidChannelNameError as e:
                    self.logger.log.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
                except IndexError:
                    self.logger.log.error(command + b" Missing parameters")
            case b"NAMES":
                try:
                    channel_name = params[0]
                    return self.command_handler.names(channel_name, connection)
                except Errors.Join.InvalidChannelNameError as e:
                    self.logger.log.error(e.message)
                    return [MessageToSend(connection.socket, e.message)]
                except IndexError:
                    self.logger.log.error(command + b" Missing parameters")
            case b"PART":
                if params:
                    try:
                        try:
                            channel_name = params[0]
                            reason = params[1]
                            return self.command_handler.part(channel_name, connection, reason)
                        except IndexError:
                            return self.command_handler.part(channel_name, connection)
                    except Errors.Part.NotOnChannelError as e:
                        self.logger.log.error(e.message)
                        return [MessageToSend(connection.socket, e.message)]
                else:
                    self.logger.log.error(command + b" Missing parameter")
            case b"PING":
                try:
                    payload = params[0]
                    return self.command_handler.ping(payload, connection)
                except IndexError:
                    self.logger.log.error(command + b" Missing parameter")
            case b"QUIT":
                try:
                    reason = params[0]
                    return self.command_handler.quit(connection, reason)
                except IndexError:
                    return self.command_handler.quit(connection)
            case _:
                self.logger.log.warning(f"Unknown command received: {command}")

    def disconnect_user(self, user: User, connection):
        user.quit_all_channels()
        self.connections.remove(connection)
        connection.is_closed = True
        user.connection_socket.close()

    def is_nickname_free(self, nickname: bytearray) -> bool:
        normalized_nickname = to_lowercase_bytes(nickname) 
        for connection in self.connections:
            if connection.user.normalized_nickname == normalized_nickname:
                return False
        return True

    def find_channel_by_name(self, channel_name: bytearray) -> Channel | None:
        for channel in self.channels:
            if channel.name == channel_name:
                return channel
        return None

    def close_connection(self, user):
        for channel in user.channels:
            channel.user_list.remove(user)

    def __format_out_log(self, msg:MessageToSend):
        connection = msg.target_socket.getsockname()
        connection_host_bytes = bytes(connection[0], "utf-8")
        connection_port_bytes = bytes(str(connection[1]), "utf-8")
        connection_addr_bytes = b"(" + connection_host_bytes + b", " + connection_port_bytes + b")"
        return connection_addr_bytes + b" -> " + msg.payload 

    def start(self):
        self.listen()
