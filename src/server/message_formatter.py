from typing import List

from server.user import User
from shared.irc_codes import IrcCodes
from shared.utils import format_byte_message


class MessageFormatter:
    class Registration:
        @staticmethod
        def RPL_WELCOME(nickname:bytearray):
            return format_byte_message(
                IrcCodes.Registration.RPL_WELCOME,
                nickname,
                b":Welcome to the Internet Relay Network",
                nickname,
            )

    class Nick:
        @staticmethod
        def NICKCHANGE(user: User):
            return format_byte_message(
                b":" + user.history.nickname[-1], b"NICK", user.nickname
            )

    class Motd:
        @staticmethod
        def RPL_MOTDSTART(nickname: bytearray, host: bytearray):
            return format_byte_message(
                b":server",
                IrcCodes.Motd.RPL_MOTDSTART,
                nickname,
                b":-",
                host,
                b"Message of the Day -",
            )

        def RPL_MOTD(nickname: bytearray, motd: bytearray):
            return format_byte_message(
                b":server",
                IrcCodes.Motd.RPL_MOTD,
                nickname,
                b":-",
                motd,
            )

        def RPL_ENDOFMOTD(nickname: bytearray):
            return format_byte_message(
                b":server",
                IrcCodes.Motd.RPL_ENDOFMOTD,
                nickname,
                b":End of /MOTD command.",
            )

    class User:
        pass

    class PingPong:
        @staticmethod
        def PING(payload):
            return f"PING :{payload}".encode()

        @staticmethod
        def PONG(payload):
            return f"PONG :{payload}".encode()

    class Names:
        @staticmethod
        def RPL_NAMREPLY(
            nickname: bytearray,
            host: bytearray,
            channel_name: bytearray,
            nickname_list: List[bytearray],
        ):
            return format_byte_message(
                b":" + host,
                IrcCodes.Names.RPL_NAMREPLY,
                nickname,
                b"=",
                channel_name,
                nickname_list,
            )

        @staticmethod
        def RPL_ENDOFNAMES(
            nickname: bytearray,
            host: bytearray,
            channel_name: bytearray,
        ):
            return format_byte_message(
                b":" + host,
                IrcCodes.Names.RPL_ENDOFNAMES,
                nickname,
                channel_name,
                b":End of /NAMES list.",
            )

    class Join:
        @staticmethod
        def JOIN_CHANNEL(nickname: bytearray, channel_name: bytearray):
            return format_byte_message(b":" + nickname, b"JOIN", b":" + channel_name)
