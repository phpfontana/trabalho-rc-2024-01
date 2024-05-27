#!/usr/bin/python

from server.server import Server

def main():
    s = Server(port=6667)
    s.start()


if __name__ == "__main__":
    main()
