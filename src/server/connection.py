from utils.logger import Logger


class Connection:

    class ConnectionConfig:
        def __init__(self):
            self.debugmode = False

    def __init__(self, conn):
        self.conn = conn
        self.buffer = ""


    def __init__(self, conn):
        self.conn = conn
        self.buffer = ""
        self.username = None

    def send_data(self, data: str):
        try:
            self.conn.sendall(data.encode())
            logging.debug(f"Data sent: {data}")
        except Exception as e:
            logging.error(f"Error while sending data: {e}")

    def incoming_data(self):
        try:
            data = self.conn.recv(512).decode()
            if not data:
                logging.warning("Received empty data")
                return False  # TODO do something when request is empty
            self.buffer += data
            logging.debug(f"Data received:{data}")
            while "\r\n" in self.buffer:
                command, params = self.parse_received_data()
                self.handle_commands(command, params)
            return True
        except Exception as e:
            logging.error(f"Error while receiving data: {e}")
            return False

    def parse_received_data(self):
        try:
            line, self.buffer = self.buffer.split("\r\n", 1)
            command, params = self.parse_command(line)
            logging.debug(f"Command parsed: {command} with params: {params}")
            return command, params
        except Exception:
            logging.error("Invalid command: \\r\\n not found")
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
            case "USER":
                self.handle_command_user(command_params)
            case "PRIVMSG":
                logging.debug("PRIVMSG command received")
            case "JOIN":
                logging.debug("JOIN command received")
            case "NAMES":
                logging.debug("NAMES command received")
            case "PART":
                logging.debug("PART command received")
            case "PING":
                logging.debug("PING command received")
                self.handle_command_ping(command_params)
            case "QUIT":
                logging.debug("QUIT command received")
            case _:
                logging.warning(f"Unknown command received: {command}")

    def handle_command_nick(self, command_params):
        nickname = command_params[0]
        if self.is_valid_nickname(nickname):
            self.nickname = nickname
            logging.info(f"Nickname set: {nickname}")
        else:
            logging.warning(f"Invalid nickname attempt: {nickname}")

    def handle_command_user(self, command_params):
        if self.is_registered():
            logging.warning("User already registered")
            return False
        else:
            self.username = command_params[0]
            logging.info(f"Username set: {self.username}")
            self.handle_command_motd()
    
    def handle_command_motd(self):
        motd_message = f":server 375 {self.nickname} :- Message of the day\r\n:server 372 {self.nickname} :- {MOTD}\r\n:server 376 {self.nickname} :End of MOTD command\r\n"
        self.send_data(motd_message)
        logging.debug(f"MOTD sent to {self.nickname}")

    def handle_command_ping(self, command_params):
        self.send_data(f"PONG :{command_params[0]}\r\n")
        logging.debug(f"PONG sent to {self.nickname}")

    def is_registered(self) -> bool:
        registered = self.nickname and self.username
        logging.debug(f"Is registered: {registered}")
        return registered

    def is_valid_nickname(self, nickname: str) -> bool:
        starts_with_letter = nickname[0].isalpha()
        on_size_limit = len(nickname) <= self.nickname_max_size
        only_alphanum_or_underline = self.is_only_alphanum_or_underline(nickname[1:])

        if starts_with_letter and on_size_limit and only_alphanum_or_underline:
            return True
        else:
            logging.warning(f"Invalid nickname: {nickname}")
            self.send_data(f'433 * {nickname} : Erroneous nickname\r\n')
            return False

    def is_only_alphanum_or_underline(self, nickname) -> bool:
        for char in nickname:
            if char.isalnum() or char == "_":
                pass
            else:
                logging.debug(f"Invalid character in nickname: {char}")
                return False
        return True
