from mypyc.test-data.fixtures.ir import bytearray
from socket import socket
from typing import List

from server.channel import Channel
from server.connection import Connection
from server.errors import Errors
from server.message_formatter import MessageFormatter
from server.message_to_send import MessageToSend
from server.user import User


class CommandHandler:
    def __init__(self, server):
        self.__server = server

    def nick(self, nickname: bytearray, connection: Connection) -> List[MessageToSend]:
        user = connection.user
        if user.is_valid_nickname(nickname):
            if self.__server.is_nickname_free(nickname):
                messages_to_send = None
                user.set_nickname(nickname)
                if not user.is_first_nick():
                    message_payload = MessageFormatter.Nick.NICKCHANGE(user)
                    messages_to_send = [
                        MessageToSend(connection.socket, message_payload)
                    ]
                    return messages_to_send
                elif user.is_registered():
                    return self.__generate_messages_for_registration(
                        connection.socket, nickname, connection.host, self.__server.motd
                    )
            else:
                raise Errors.Nickname.NicknameAlreadyInUseError(nickname)
        else:
            raise Errors.Nickname.InvalidNicknameError(nickname)

    def user(self, username: bytearray, connection: Connection) -> List[MessageToSend]:
        user = connection.user
        if not user.username:
            user.username = username
            if user.is_registered():
                return self.__generate_messages_for_registration(
                    connection.socket,
                    user.nickname,
                    connection.host,
                    self.__server.motd,
                )
        else:
            self.__server.logger.warning("change realname attempt")
            raise "change realname attempt"

    def ping(self, payload: bytearray, connection: Connection) -> List[MessageToSend]:
        if payload:
            message_payload = MessageFormatter.PingPong.PONG(payload)
            messages_to_send = [MessageToSend(connection.socket, message_payload)]
            return messages_to_send
        else:
            raise "ping without payload"

    def join(self, channel_name: bytearray, connection: Connection):
        user = connection.user
        new_channel = Channel(channel_name)
        if new_channel.is_valid_channel_name(channel_name):
            channel = self.__server.find_channel_by_name(new_channel.normalized_name)
            if channel:
                channel.user_list.append(user)
                messages_to_send = self.__generate_messages_for_channel_join(
                    user, connection.host, channel
                )
                return messages_to_send
            else:
                self.__server.channels.append(new_channel)
                messages_to_send = self.__generate_messages_for_channel_join(
                    user, connection.host, new_channel
                )
                return messages_to_send
        else:
            raise Errors.Join.InvalidChannelNameError(connection.host, channel_name)

    def privmsg(
        self, channel_name: bytearray, user_msg: bytearray, connection: Connection
    ):
        nickname: bytearray = connection.user.nickname
        channel = self.__server.find_channel_by_name(channel_name)
        if channel:
            privmsg = MessageFormatter.Privmsg.PRIVMSG(nickname, channel_name, user_msg)
            messages_to_send = []
            for user in channel.user_list:
                messages_to_send.append(MessageToSend(user.connection_socket, privmsg))
            return messages_to_send
        else:
            raise Errors.Join.InvalidChannelNameError(connection.host, channel_name)

    def part(
        self, channel_name: bytearray, connection, reason: bytearray = bytearray()
    ):
        user = connection.user
        channel = self.__server.find_channel_by_name
        if channel:
            partmsg = MessageFormatter.Part.PART_CHANNEL(
                user.nickname, channel_name, reason
            )
            messages_to_send = []
            for user in channel.user_list:
                messages_to_send.append(MessageToSend(user.connection_socket, partmsg))
            return messages_to_send
        else:
            raise Errors.Part.NotOnChannelError(
                user.nickname, connection.host, channel_name
            )

    def names(self, channel_name: bytearray, connection):
        user = connection.user
        channel = self.__server.find_channel_by_name(channel_name)
        socket = connection.socket
        if channel:
            host = connection.host
            nickname_list = channel.get_nick_name_list()
            msg_list = MessageFormatter.Names.RPL_NAMREPLY(
                user.nickname, host, channel.name, nickname_list
            )
            msg_list_end = MessageFormatter.Names.RPL_ENDOFNAMES(
                user.nickname, host, channel.name
            )
            return [
                MessageToSend(socket, msg_list),
                MessageToSend(socket, msg_list_end),
            ]
        else:
            raise Errors.Join.InvalidChannelNameError(connection.host, channel_name)

    def quit(self, reason: bytearray=bytearray(), connection):
        user = connection.user
        msg_quit = MessageFormatter.Quit.QUIT_SERVER(user.nickname, reason)
        messages_to_send = []
        for connection in self.__server.connections:
            messages_to_send.append(MessageToSend(connection.socket, msg_quit))
        return messages_to_send

    def __generate_messages_for_registration(
        self, socket: socket, nickname: bytearray, host: bytearray, motd: bytearray
    ) -> List[MessageToSend]:
        welcome_msg = MessageToSend(
            socket, MessageFormatter.Registration.RPL_WELCOME(nickname)
        )
        motd_start_msg = MessageToSend(
            socket, MessageFormatter.Motd.RPL_MOTDSTART(nickname, host)
        )
        motd_msg = MessageToSend(socket, MessageFormatter.Motd.RPL_MOTD(nickname, motd))
        motd_end_msg = MessageToSend(
            socket, MessageFormatter.Motd.RPL_ENDOFMOTD(nickname)
        )
        return [welcome_msg, motd_start_msg, motd_msg, motd_end_msg]

    def __generate_messages_for_channel_join(
        self, user: User, host: bytearray, channel: Channel
    ) -> List[MessageToSend]:
        nickname_list = channel.get_nickname_list()
        message_join = MessageFormatter.Join.JOIN_CHANNEL(user.nickname, channel.name)
        message_list = MessageFormatter.Names.RPL_NAMREPLY(
            user.nickname, host, channel.name, nickname_list
        )
        message_list_end = MessageFormatter.Names.RPL_ENDOFNAMES(
            user.nickname, host, channel.name
        )
        messages_to_send = self.__generate_messages_to_send_list_for_channel_join(
            user, channel, message_join, message_list, message_list_end
        )
        return messages_to_send

    def __generate_messages_to_send_list_for_channel_join(
        self,
        user: User,
        channel: Channel,
        message_join: bytearray,
        message_list: bytearray,
        message_list_end: bytearray,
    ):
        messages_to_send = []
        for user in channel.user_list:
            messages_to_send.append(MessageToSend(user.connection_socket, message_join))
        messages_to_send.append(MessageToSend(user.connection_socket, message_list))
        messages_to_send.append(MessageToSend(user.connection_socket, message_list_end))
        return messages_to_send

    # def __generate_messages_to_send_list_for_channel_msg(self, nickname:bytearray, channel_name:bytearray, msg:bytearray):
