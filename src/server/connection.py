from socket import socket
from typing import List

from server.errors import Errors
from server.processed_message import ProcessedMessage
from server.user import User
from shared.logger import Logger


class Connection:
    class ConnectionConfig:
        def __init__(self, debug_mode=False):
            self.debugmode = debug_mode

    def __init__(self, socket: socket, debug_mode:bool=False):
        self.socket = socket
        self.host = socket.getsockname()[0].encode()
        self.buffer = bytearray()
        self.message_history: List[ProcessedMessage] = []
        self.configuration = self.ConnectionConfig(debug_mode)
        self.user = User(socket, debug_mode=debug_mode)
        self.logger = Logger(".server.log", debug_mode)

    def send_data(self, data: bytes):
        try:
            self.socket.sendall(data.encode())
            self.logger.debug(f"Data sent: {data}")
        except Exception as e:
            self.logger.error(f"Error while sending data: {e}")

    def wait_for_message(self) -> ProcessedMessage:
        try:
            if not self.buffer:
                data_chunk = self.socket.recv(512)
                if data_chunk == b"":
                    raise "connecton closed"
                self.buffer.extend(data_chunk)
            processed_message = ProcessedMessage(self.buffer)
            self.buffer = processed_message.remaining_buffer
            self.message_history.append(processed_message)
            return processed_message
        except Errors.NoEndMessageCharsFoundError:
            return False

    def parse_received_data(self):
        try:
            line, self.buffer = self.buffer.split("\r\n", 1)
            command, params = self.parse_command(line)
            return command, params
        except Exception:
            raise "INVALID COMMAND: \\r\\n not found"
