#!/usr/bin/python

import socket
import queue
import time
from random import randint
from collections import deque
from _thread import *
from client_server import Client

# Mensagem do Dia
MOTD = """servidor"""


class Server:

    def __init__(self, port=6667):
        # Sempre que precisar de uma estrutura de dados que poderá ser acessada em diferentes conexões,
        # utilize apenas deque ou queue. Exemplo, para armazenar as conexões ativas:
        self.conns = deque()
        self.port = port

    def run(self, conn):
        client = Client(conn)
        while client.incoming_data():
            pass

    def listen(self):
        """(não alterar)
        Escuta múltiplas conexões na porta definida, chamando o método run para
        cada uma. Propriedades da classe Servidor são vistas e podem
        ser alteradas por todas as conexões.
        """

        # Cria o socket
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Permite reuso do endereço
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Faz o bind do socket - associa o socket com o endereço e porta
        _socket.bind(("", self.port))

        # Escuta até 4096 conexões
        _socket.listen(4096)

        # Aceita conexões
        while True:
            print(f"Servidor aceitando conexões na porta {self.port}...")
            client, addr = _socket.accept()
            start_new_thread(self.run, (client,))

    def start(self):
        """(não alterar)
        Inicia o servidor no método listen e fica em loop infinito.
        """
        self.listen()

def main():
    s = Server(port=6667)
    s.start()


if __name__ == "__main__":
    main()
