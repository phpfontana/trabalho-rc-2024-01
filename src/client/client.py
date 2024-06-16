#!/usr/bin/python

import socket
from time import time
from src.client.user import User
from typing import Tuple

class Client():
    def __init__(self, ip=""):
        self.connected = False
        self.host = None
        self.port = None
        self.server_socket = None
        self.ping_socket = None
        self.user = User()

    def connect_to_server(self, server_addr:Tuple[str,int]):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.connect(server_addr)
        self.server_socket = _socket
        self.host, self.port = _socket.getsockname()
        self.connected = True


def main():
    c = Client()
    c.connect_to_server()


if __name__ == '__main__':
    main()
