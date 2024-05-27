import socket
from _thread import start_new_thread
from collections import deque
from server.connection import ClientConnection


class Server:
    def __init__(self, port=6667, debug_mode=False):
        self.connections = deque()
        self.port = port
        self.message_of_the_day = "Welcome to the Internet Relay Network"
        self.debug_mode = debug_mode

    def run(self, connection):
        client = ClientConnection(connection, self.message_of_the_day, self.debug_mode)
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


