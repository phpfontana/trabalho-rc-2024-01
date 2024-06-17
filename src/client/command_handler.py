import os
import socket
from datetime import datetime
from typing import List

from client.channel import Channel
from client.errors import (
    CommandOnlyUsableConnectedError,
    InvalidChannelNameError,
    InvalidNicknameError,
    SendDataToServerError,
)
import logging


class CommandHandler:
    def __init__(self, client , user, logger):
        self.client = client
        self.user = user
        self.logger = logger

    def help(self):
        commands = {
            "/help": "List all available commands with a brief description of each.",
            "/nick": "Change the user nickname. Usage: /nick <new_nickname>",
            "/connect": "Connect to the server. Usage: /connect <IP> <PORT>",
            "/disconnect": "Disconnect from the server. Usage: /disconnect :<reason>",
            "/quit": "Exit the client. Usage: /quit :<reason>",
            "/join": "Join a channel. Usage: /join #<channel>",
            "/leave": "Leave a channel. Usage: /leave #<channel> <reason>",
            "/channel": "Select a default channel. Usage: /channel #<channel>",
            "/list": "List the users in a channel. Usage: /list #<channel>",
            "/msg": "Send a message to a channel. Usage: /msg #<channel> <message>",
        }
        for command, description in commands.items():
            print(f"{command}: {description}")

    def connect(self, addr):  # TODO Exception already connected to server
        if not self.user.nickname:
            print("Set a nickname before connection")
            return
        retry = 3
        while retry:
            try:
                retry -= 1
                self.client.connect_to_server((addr))
                self.__send_to_server(self.__format_registration_msg())
                return
            except SendDataToServerError as e:
                print(e.msg)
            except socket.error as e:
                print("Erro tentar se conectar ao servidor!")
                print(e)
                print(f"Retry {retry}")

    def nick(self, nickname: str):
        try:
            self.user.set_nickname(nickname)
            if self.client.connected and self.user.is_registered():
                msg = self.__format_nick_msg()
                self.logger.log_colored.in_(logging.INFO, f"NICK OUT: {msg}")
                self.__send_to_server(msg)
            else:
                print("You are not connected to any server!")
                print(f"Nick setted locally to {self.user.nickname}!")
        except InvalidNicknameError as e:
            print(e.msg)

    def list(self, channel_name: str = None):
        if self.client.connected:
            if not channel_name:
                if self.user.default_channel:
                    channel_name = self.user.default_channel
                else:
                    print("U DONT HAVE DEFAULT CHANNEL")
                    return
            self.__send_to_server(self.__format_names_msg(channel_name))
        else:
            raise CommandOnlyUsableConnectedError("/list")

    def msg(self, msg: str, channel_name: str = None):
        if self.client.connected:
            if not channel_name:
                if self.user.default_channel:
                    channel_name = self.user.default_channel.name
                else:
                    print("U DONT HAVE DEFAULT CHANNEL")
                    return
            self.print_msg(channel_name, self.user, msg)
            self.__send_to_server(self.__format_privmsg_msg(channel_name, msg))
        else:
            raise CommandOnlyUsableConnectedError("/list")

    def channel(self, channel_name: str = None):
        if not channel_name:
            if self.user.channels:
                print("Channels: ")
                for channel in self.user.channels:
                    print(channel.name, end=" ")
            else:
                raise CommandOnlyUsableConnectedError("/channel")
        else:
            self.user.default_channel = channel_name
            print(f"Congrats! You have set {channel_name} as your default channel!")

    def disconnect(self, reason: str = None):
        if self.client.connected:
            self.__send_to_server(self.__format_quit_msg(reason))
            self.client.server_socket.close()
            self.client.connected = False
        else:
            raise CommandOnlyUsableConnectedError("/disconnect")

    def quit(self, reason: str):
        self.client.server_socket.close()
        os._exit(0)

    def leave(self, channel_name: str, reason: str = None):
        if self.client.connected:
            if not channel_name:
                channel_name = self.user.default_channel
            self.__send_to_server(self.__format_part_msg(channel_name, reason))
        else:
            raise CommandOnlyUsableConnectedError("/disconnect")

    def join(self, channel_name: str):
        if self.client.connected:
            try:
                new_channel = Channel(channel_name)
                self.user.join_channel(new_channel)
                self.__send_to_server(self.__format_join_msg(channel_name))
            except InvalidChannelNameError as e:
                print(e.msg)
        else:
            raise CommandOnlyUsableConnectedError("/disconnect")

    def print_msg(self, nickname: str, channel_name: str, msg: str):
        hour_minute = datetime.now().strftime("%H:%M")
        print(f"{hour_minute} [{channel_name}] <{nickname}> {msg}\r\n")

    def __format_privmsg_msg(self, channel_name: str, msg: str):
        return f"PRIVMSG {channel_name} :{msg}\r\n".encode()

    def __format_part_msg(self, channel_name, reason: str = None):
        if not reason:
            return f"PART {channel_name}\r\n".encode()
        else:
            return f"PART {channel_name} :{reason}\r\n".encode()

    def __format_nick_msg(self):
        return f"NICK {self.user.nickname}\r\n".encode()

    def __format_join_msg(self, channel_name: str):
        return f"JOIN {channel_name}\r\n".encode()

    def __format_user_msg(self):
        return f"USER {self.user.nickname}\r\n".encode()

    def __format_registration_msg(self):
        return self.__format_nick_msg() + self.__format_user_msg()

    def __format_names_msg(self, channel_name: str):
        return f"NAMES {channel_name}\r\n".encode()

    def __format_quit_msg(self, reason: str = None):
        if not reason:
            return "QUIT\r\n".encode()
        else:
            return f"QUIT :{reason}\r\n".encode()

    def __send_to_server(self, msg):
        self.client.server_socket.sendall(msg)
