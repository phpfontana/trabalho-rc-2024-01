from typing import List
from shared.utils import format_byte_message
from server.user import User
from shared.irc_codes import IrcCodes


class MessageFormatter:
    class Registration:
        def RPL_WELCOME(self, user: User, host: str, motd: str):
            welcome_msg = (
                f"{IrcCodes.Registration.RPL_WELCOME} {user.nickname} :Welcome to the"
                f" Internet Relay Network {user.nickname}\r\n"
            )
            motd_msg = (
                f":server {IrcCodes.Motd.RPL_MOTDSTART} {user.nickname} :-"
                f" {host} Message of the Day -\r\n:server"
                f" {IrcCodes.Motd.RPL_MOTD} {user.nickname} :- {motd}\r\n:server"
                f" {IrcCodes.Motd.RPL_ENDOFMOTD} {user.nickname} :End of /MOTD"
                " command.\r\n"
            )
            return (welcome_msg + motd_msg).encode()

    class Nick:
        def NICKCHANGE(self, user: User):
            return f":{user.history.nickname[-1]} NICK {user.nickname}\r\n".encode()

    class User:
        pass

    class PingPong:
        def PING(self, payload):
            return f"PING :{payload}".encode()

        def PONG(self, payload):
            return f"PONG :{payload}".encode()

    class Names:
        def RPL_NAMREPLY(
            self,
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

        def RPL_ENDOFNAMES(
            self,
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
        def JOIN_CHANNEL(self, nickname: bytearray, channel_name: bytearray):
            return format_byte_message(
                b":" + nickname, b"JOIN", b":" + channel_name
            )

