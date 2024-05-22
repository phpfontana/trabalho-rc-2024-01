#!/usr/bin/python

import socket
import queue
import time
from collections import deque
from _thread import *

# Mensagem do Dia 
MOTD = '''servidor'''

class Cliente:
    def __init__(self, conn, server):
        self.conn = conn        # The socket connection to the client
        self.server = server    # The server object
        self.buffer = ''        # Stores received data temporarily
        self.nick = None        # Store client's nickname
        self.username = None    # Store client's username

    def incoming_data(self):
        """
        Receives data from the client. 
        If data is received, it splits the buffer by newline characters and processes each command
        """
        try:
            # Attempt to receive up to 1024 bytes of data from the client
            data = self.conn.recv(1024).decode()
            # If no data is received
            if not data:
                return False   
            # Append received data to the buffer
            self.buffer += data
            # Process each command in the buffer
            while '\r\n' in self.buffer:
                # Splits buffer into a command and the rest
                line, self.buffer = self.buffer.split('\r\n', 1)
                # Handle data
                self.handle_data(line)
            return True
        except:
            return False
    
    def handle_data(self, line):
        if line.startswith("NICK"):
            self.handle_nick_name(line)

        elif line.startswith('USER'):
            self.handle_username(line)
    
    def handle_nickname(self, line):
        # Splits the line into ["NICK", "nickname"]
        parts = line.split()

        # Verify if nickname is provided
        if len(parts) < 2:
            return

        # Store the nickname
        new_nickname = parts[1]

        if new_nickname[0].isnum() or not new_nickname.isalnum() or len(new_nickname) > 9:

        
    def enviar_dados(self, msg):
        pass

class Servidor:
    def __init__(self, port=6667):
        # Sempre que precisar de uma estrutura de dados que poderá ser acessada em diferentes conexões, 
        # utilize apenas deque ou queue. Exemplo, para armazenar as conexões ativas:
        self.conns = deque()
        self.port = port
    
    def run(self, conn):
        Cliente(conn)
        pass

    def listen(self):
        '''(não alterar)
        Escuta múltiplas conexões na porta definida, chamando o método run para
        cada uma. Propriedades da classe Servidor são vistas e podem 
        ser alteradas por todas as conexões.
        '''

        # Cria o socket
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   

        # Permite reuso do endereço
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

        # Faz o bind do socket - associa o socket com o endereço e porta
        _socket.bind(('', self.port))

        # Escuta até 4096 conexões
        _socket.listen(4096)

        # Aceita conexões
        while True:
            print(f'Servidor aceitando conexões na porta {self.port}...')
            client, addr = _socket.accept()
            start_new_thread(self.run, (client, ))

    def start(self):
        '''(não alterar)
        Inicia o servidor no método listen e fica em loop infinito.
        '''
        start_new_thread(self.listen, ())

        while True:
            time.sleep(60)
            print('Servidor funcionando...')


def main():
    s = Servidor(port=6667)
    s.start()

if __name__ == '__main__':
    main()
    