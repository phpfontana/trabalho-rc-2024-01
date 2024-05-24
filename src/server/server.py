#!/usr/bin/python

import socket
import queue
import time
from random import randint
from collections import deque
from _thread import start_new_thread
from client_connection import Connection

# Mensagem do Dia
MOTD = """servidor"""


class Server:

    def __init__(self, port=6667):
        self.conns = deque()
        self.port = port

    def run(self, conn):
        client = Connection(conn)
        while client.incoming_data():
            pass

    def listen(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.bind(("", self.port))
        _socket.listen(4096)

        while True:
            print(f"Servidor aceitando conexões na porta {self.port}...")
            connection_socket, addr = _socket.accept()
            start_new_thread(self.run, (connection_socket,))

    def start(self):
        self.listen()


def main():
    s = Server(port=6667)
    s.start()


if __name__ == "__main__":
    main()
