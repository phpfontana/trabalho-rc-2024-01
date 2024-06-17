#!/usr/bin/python

from client.client import Client

def main():
    c = Client(enabled=True)
    c.start()



if __name__ == '__main__':
    main()
