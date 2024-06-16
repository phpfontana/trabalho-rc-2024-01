#!/usr/bin/python

from client.client import Client

def main():
    c = Client()
    c.input_handler.listen_command_input()



if __name__ == '__main__':
    main()
