from server.connection import ClientConnection

class ProcessedMessage():
    def __init__(self, buffer:bytearray):
        self.data_buffer = buffer
        self.message = self.__separate_message(buffer)
        self.command, self.params = self.__parse_message()

    def __separate_message(self):
        if "\r\n" in self.data_buffer.buffer:
            message, self.data_buffer  = self.data_buffer.split(b"\r\n",1)
            return message
        else:
            raise "erro de não tem \r\n"

    def __parse_message(self):
        command, params = self.message.split(b" ",1)
        if not isinstance(self.params, list):
            self.params = list(self.params)
        return command, params
