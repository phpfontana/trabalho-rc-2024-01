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
        self.logger.log.debug(message)
        self.logger.log.debug(message[0])
        if message[0] == 58:
            self.logger.log.debug("entrei")
            splited_message = message.split(b" ")
            if splited_message[1] == b"NICK":
                return b"NICK"
            if splited_message[1] == b"PRIVMSG":
                return b"PRIVMSG"
            if splited_message[1] == b"QUIT":
                return b"QUIT"
            if splited_message[1] == b"PART":
                return b"PART"
            if splited_message[1] == b"JOIN":
                return b"JOIN"
            self.logger.log.debug("baixo")
            splited_message = message.split(b" ",1)
            self.logger.log.debug(splited_message)
            three_digits_pattern = rb'(?<!\d)\d{3}(?!\d)'
            irc_commands_pattern = rb'\b(USER|NICK|PING|PONG|JOIN|PART|QUIT|PRIVMSG|NAMES)\b'
            combined_pattern = re.compile(rb'%s|%s' % (three_digits_pattern, irc_commands_pattern))
            match = combined_pattern.search(splited_message[1])
            if match:
                return match.group(0)
            else:
                return None
        self.logger.log.debug("reto")
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
