class ProcessedMessage():
    def __init__(self, buffer:bytearray):
        self.remaining_buffer = buffer
        self.message = self.__separate_message()
        self.command, self.params = self.__parse_message()

    def __separate_message(self):
        if b"\r\n" in self.remaining_buffer:
            message, self.remaining_buffer  = self.remaining_buffer.split(b"\r\n",1)
            return message
        else:
            raise "erro de não tem \r\n"

    def __parse_message(self):
        command, params = self.message.split(b" ",1)
        if not isinstance(params, list):
            params = [params]
        return command, params
