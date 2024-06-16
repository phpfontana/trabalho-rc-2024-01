from socket import socket
from typing import List

from server.errors import Errors
from server.processed_message import ProcessedMessage
from server.user import User
import logging


class Connection:
    def __init__(self, socket: socket, addr, server):
        self.__server = server
        self.is_closed = False
        self.socket = socket
        self.addr = addr
        self.host = socket.getsockname()[0].encode()
        self.buffer = bytearray()
        self.message_history: List[ProcessedMessage] = []
        self.user = User(socket)

    def send_data(self, data: bytes):
        try:
            self.socket.sendall(data.encode())
            self.__server.logger.log.debug(f"Data sent: {data}")
        except Exception as e:
            self.__server.logger.log.error(f"Error while sending data: {e}")

    def wait_for_message(self) -> ProcessedMessage:
        try:
            if not self.buffer:
                if not self.is_closed:
                    data_chunk = self.socket.recv(512)
                    self.__server.logger.log_colored.in_(logging.INFO, data_chunk)
                    if data_chunk == b"":
                        raise Errors.Connection.ConnectionClosedByPeer(self)
                self.buffer.extend(data_chunk)
            processed_message = ProcessedMessage(self.buffer, self.__server.logger)
            self.buffer = processed_message.remaining_buffer
            self.message_history.append(processed_message)
            return processed_message
        except Errors.NoEndMessageCharsFoundError:
            return False

    def close(self):
        self.user.quit()
        self.socket.close()

    def parse_received_data(self):
        try:
            line, self.buffer = self.buffer.split("\r\n", 1)
            command, params = self.parse_command(line)
            return command, params
        except Exception:
            raise "INVALID COMMAND: \\r\\n not found"
