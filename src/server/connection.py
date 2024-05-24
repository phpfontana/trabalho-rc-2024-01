from pprint import pprint


class Connection:
    def __init__(self, conn):
        self.conn = conn
        self.buffer = ""

    def incoming_data(self):
        try:
            data = self.conn.recv(1024).decode()
            if not data:
                return False
            self.buffer += data
            while "\r\n" in self.buffer:
                command, params = self.parse_received_data()
                self.handle_commands(command, params)
            return True
        except Exception:
            return False

    def parse_received_data(self):
        try:
            line, self.buffer = self.buffer.split("\r\n", 1)
            command, params = self.parse_command(line)
            return command, params
        except Exception:
            raise "INVALID COMMAND: \\r\\n not found"

    def parse_command(self, line: str) -> list:
        command, params = line.split(" ", 1)
        if " " in params:
            params = params.split(" ")
        else:
            params = [params]
        return command, params

    def handle_commands(self, command, command_params):
        match command:
            case "NICK":
                self.handle_command_nick(command_params)
                pass
            case "USER":
                self.handle_command_user(command_params)
                pass
            case "PRIVMSG":
                pass
            case "JOIN":
                pass
            case "NAMES":
                pass
            case "PART":
                pass
            case "MOTD":
                pass
            case "PING":
                pass
            case "QUIT":
                pass
