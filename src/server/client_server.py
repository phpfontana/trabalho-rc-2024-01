from pprint import pprint
class Client:
    def __init__(self, conn):
        self.conn = conn
        self.buffer = ""
        self.nickname = None
        self.nickname_max_size = 9
        self.username = None

    def incoming_data(self):
        print("fui chamado")
        try:
            data = self.conn.recv(1024).decode()
            if not data:
                return False  # TODO do something when request is empty
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
        pprint(vars(self))

    def handle_command_nick(self, command_params):
        nickname = command_params[0]
        if self.is_valid_nickname(nickname):
            self.nickname = nickname
        else:
            return False

    def handle_command_user(self, command_params):
        if self.is_registered():
            return False
        else:
            self.username = command_params[0]

    def is_registered(self) -> bool:
        if self.nickname and self.username:
            return True
        else:
            return False

    def is_valid_nickname(self, nickname: str) -> bool:
        starts_with_letter = nickname[0].isalpha()
        on_size_limit = len(nickname) <= self.nickname_max_size
        only_alphanum_or_underline = self.is_only_alphanum_or_underline(nickname[1:])

        if starts_with_letter and on_size_limit and only_alphanum_or_underline:
            return True
        else:
            return False

    def is_only_alphanum_or_underline(self, nickname) -> bool:
        for char in nickname:
            if char.isalnum() or char == "_":
                pass
            else:
                return False
        return True
