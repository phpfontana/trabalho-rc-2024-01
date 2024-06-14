from socket import socket

class MessageToSend:
    def __init__(self, target_socket: socket, payload: bytes):
        self.target_socket = target_socket
        self.payload = payload

    def send(self):
        self.target_socket.sendall(self.payload)
