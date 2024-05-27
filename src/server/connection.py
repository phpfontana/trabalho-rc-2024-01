from typing import Any

from server.errors import InvalidNicknameError
from server.user import User
from utils.logger import Logger


class ClientConnection:
    class ConnectionConfig:
        def __init__(self, debug_mode=False):
            self.debugmode = debug_mode

    def __init__(self, connection_socket, message_of_the_day, debug_mode=False):
        self.connection_socket = connection_socket
        self.buffer = ""
        self.configuration = self.ConnectionConfig(debug_mode)

        self.user = User(debug_mode=debug_mode)
        self.logger = Logger(".server.log", debug_mode)

    def send_data(self, data: str):
        try:
            self.connection_socket.sendall(data.encode())
            self.logger.debug(f"Data sent: {data}")
        except Exception as e:
            self.logger.error(f"Error while sending data: {e}")

    def incoming_data(self):
        try:
            data = self.connection_socket.recv(512).decode()
            if not data:
                self.logger.warning("Received empty data")
                return False  # TODO do something when request is empty
            self.buffer += data
            self.logger.debug(f"Data received:{data}")
            while "\r\n" in self.buffer:
                command, params = self.parse_received_data()
                self.handle_commands(command, params)
            return True
        except Exception as e:
            self.logger.error(f"Error while receiving data: {e}")
            return False

    def parse_received_data(self):
        try:
            line, self.buffer = self.buffer.split("\r\n", 1)
            command, params = self.parse_command(line)
            self.logger.debug(f"Command parsed: {command} with params: {params}")
            return command, params
        except Exception:
            self.logger.error("Invalid command: \\r\\n not found")
            raise "INVALID COMMAND: \\r\\n not found"

    def parse_command(self, line: str) -> tuple[str, list[str]]:
        params:Any
        command, params = line.split(" ", 1)
        if " " in params:
            params = params.split(" ")
        else:
            params = [params]
        return command, params

    def handle_commands(self, command, command_params):
        match command:
            case "NICK":
                self.logger.debug("NICK command received")
                try:
                    nickname = command_params[0]
                    nick_message = self.user.handle_command_nick(nickname)
                    self.send_data(nick_message)
                except InvalidNicknameError as e:
                    self.send_data(e.message)
            case "USER":
                self.logger.debug("USER command received")
                self.user.handle_command_user(command_params)
                motd_response = self.user.handle_command_motd(command_params)
                self.send_data(motd_response)
            case "MOTD":
                motd = self.user.handle_command_motd(command_params)
                self.send_data(motd)
                self.logger.debug("MOTD command received")
            case "PRIVMSG":
                self.logger.debug("PRIVMSG command received")
            case "JOIN":
                self.logger.debug("JOIN command received")
            case "NAMES":
                self.logger.debug("NAMES command received")
            case "PART":
                self.logger.debug("PART command received")
            case "PING":
                self.logger.debug("PING command received")
                self.user.handle_command_ping(command_params)
            case "QUIT":
                self.logger.debug("QUIT command received")
            case _:
                self.logger.warning(f"Unknown command received: {command}")
