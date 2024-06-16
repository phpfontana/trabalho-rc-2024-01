from typing import List
from typing import Tuple
from typing import Any
import re


class ProcessedMessage:
    def __init__(self, buffer: bytearray, logger):
        self.remaining_buffer = buffer
        self.logger = logger
        self.message = self.__separate_message()
        self.command_or_code = self.find_three_digits_or_irc_command_bytes(buffer)


    def find_three_digits_or_irc_command_bytes(self, message):
        if message[0] == b":":
            splited_message = message.split(" ")
            if splited_message[1] == b"NICK":
                return b"NICK"
        three_digits_pattern = rb'(?<!\d)\d{3}(?!\d)'
        irc_commands_pattern = rb'\b(USER|NICK|PING|PONG|JOIN|PART|QUIT|PRIVMSG|NAMES)\b'
        combined_pattern = re.compile(rb'%s|%s' % (three_digits_pattern, irc_commands_pattern))
        match = combined_pattern.search(message)
        if match:
            return match.group(0)
        else:
            return None

    def __separate_message(self):
        if b"\r\n" in self.remaining_buffer:
            message, self.remaining_buffer = self.remaining_buffer.split(b"\r\n", 1)
            return message
        else:
            raise "erro de não tem \r\n"


    def __parse_message(self) -> Tuple[str, List[bytearray]]:
        if b" " in self.message:
            command, params = self.message.split(b" ", 1)
            params_list = self.__parse_params(params)
            return (command, params_list)
        else:
            return (self.message, [])

    def __parse_params(self, params:bytearray) -> List[bytearray]:
        text_param: Any # bytearray/bytes LSP is crying
        if b" :" in params:
            other_params, text_param = params.split(b" :", 1)
            text_param = b":" + text_param
            other_params = other_params.strip()
            self.logger.log.debug(other_params)
            self.logger.log.debug(text_param)
            if other_params:
                if b" " in other_params:
                    other_params_list = other_params.split(b" ")
                    return other_params_list + [text_param]
                else:
                    return [other_params, text_param]
            else:
                return [text_param]
        else:
            if b" " in params:
                return params.split(b" ")
            else:
                return [params]
