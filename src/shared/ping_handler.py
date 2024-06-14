from random import randbytes


class PingHandler:
    class Ping:
        def __init__(self, ping_handler: "PingHandler"):
            self.ping_handler = ping_handler

        def generate_ping_msg(self):
            self.ping_handler.payload = self.__generate_payload()
            return f"PING :{self.ping_command.payload}"

        def __generate_payload(self):
            return randbytes(4)

    class Pong:
        def __init__(self, ping_handler: "PingHandler"):
            self.ping_command = ping_handler

        def generate_pong_msg(self):
            return f"PONG :{self.ping_command.payload}"

    def __init__(self):
        self.payload = None
        self.ping = self.Ping(self)
        self.pong = self.Pong(self)
