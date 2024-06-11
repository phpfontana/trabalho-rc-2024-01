#!/usr/bin/python

import socket
import threading
from time import time
from shared.users import User

class Client():
    def __init__(self, ip="localhost:6667"):
        self.connected = False
        self.ip = ip
        self.socket = None
        self.user = User()

    def connect_to_server(self):
        print('Cliente!')
        while True:
            try:
                cmd = input()
            except Exception as e:
                pass


def main():
    c = Client()
    c.connect_to_server()


if __name__ == '__main__':
    main()
