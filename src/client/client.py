import socket
from _thread import start_new_thread
from time import time
from client.user import User
from typing import Tuple
from shared.logger import Logger
import logging
from client.input_handler import InputHandler
from client.message_receiver import MessageReceiver

class Client():
    def __init__(self, ip="", enabled=False):
        self.connected = False
        self.host = None
        self.port = None
        self.server_socket = None
        self.ping_socket = None
        self.logger = Logger(level=logging.DEBUG, enabled=enabled)
        self.user = User()
        self.input_handler = InputHandler(self, self.user, self.logger)
        self.message_receiver = MessageReceiver(self, self.user, self.logger)

    def connect_to_server(self, server_addr:Tuple[str,int]):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.connect(server_addr)
        self.server_socket = _socket
        self.host, self.port = _socket.getsockname()
        self.logger.log.debug("startou a thread")
        start_new_thread(self.server_listener_thread, ())

    def start(self):
        start_new_thread(self.ping_sender_thread, ())
        self.input_listener_thread()

    def input_listener_thread(self):
        self.input_handler.listen_command_input()

    def server_listener_thread(self):
        self.message_receiver.listen_server_messages()

    def ping_sender_thread(self):
        pass
