from typing import Any

from utils.logger import Logger

from server.errors import InvalidNicknameError
from server.errors import NoEndMessageCharsFoundError
from server.processed_message import ProcessedMessage
from shared.user import User
from typing import List
from socket import socket


class ClientConnection:
    class ConnectionConfig:
        def __init__(self, debug_mode=False):
            self.debugmode = debug_mode

    def __init__(self, connection_socket: socket, debug_mode=False):
        self.socket = connection_socket
        self.host = connection_socket.getsockname()[0].encode()
        self.buffer = bytearray()
        self.message_history:List[ProcessedMessage] = []
        self.configuration = self.ConnectionConfig(debug_mode)
        self.user = User(debug_mode=debug_mode)
        self.logger = Logger(".server.log", debug_mode)

    def send_data(self, data: bytes):
        try:
            self.socket.sendall(data.encode())
            self.logger.debug(f"Data sent: {data}")
        except Exception as e:
            self.logger.error(f"Error while sending data: {e}")

    def wait_for_message(self) -> ProcessedMessage:
        try:
            data_chunk = self.socket.recv(512)
            if data_chunk == b"":
                raise "connecton closed"
            self.buffer.extend(data_chunk)
            processed_message = ProcessedMessage(self.buffer)
            self.message_history.append(processed_message)
            return processed_message
        except NoEndMessageCharsFoundError:
            return True
        except Exception as e:
            self.logger.error(f"Error while receiving data: {e}")
            return False

    def parse_received_data(self):
        try:
            line, self.buffer = self.buffer.split("\r\n", 1)
            command, params = self.parse_command(line)
            return command, params
        except Exception:
            raise "INVALID COMMAND: \\r\\n not found"
