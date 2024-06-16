#!/usr/bin/python

import socket
from time import time
from shared.users import User
from typing import Tuple

class Client():
    def __init__(self, ip="localhost:6667"):
        self.connected = False
        self.ip = ip
        self.server_socket = None
        self.ping_socket = None
        self.user = User()

    def connect_to_server(self, server_addr:Tuple(str,int)):
        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            _socket.connect(server_addr)
        except Exception as e:
            print("Erro tentar se conectar ao servidor!")
            print(e)


def main():
    c = Client()
    c.connect_to_server()


if __name__ == '__main__':
    main()
