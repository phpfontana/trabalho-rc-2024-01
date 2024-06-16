# Trabalho Redes de Computadores - 2024/01

## 1. Visão geral
**Nome do Projeto:** Internet Relay Chat (IRC)

**Descrição:** Este projeto é uma implementação de um servidor IRC que permite aos usuarios se conectarem em canais e se cmunicarem usando vários comandos.

## 2. Configuração

**Pré-requisitos:**
*   Python 3.8 ou superior

**Instalação:**
1. Clone o repositório
```sh
git clone https://github.com/phpfontana/trabalho-rc-2024-01.git
cd trabalho-rc-2024-01
```
Instalação de pacotes não é necessário.

## 3. Modulos

### 3.1 Modulo Server

#### 3.1.1 `server.py`
A classe `Server` é a classe principal que inicializa e executa o servidor IRC. Ela é responsável por genrenciar as conexões dos clientes, canais e processa comandos do cliente.

**Atributos:**
- `port`: O número da porta na qual o servidor escuta.
- `connections`: Um deque que armazena as conexões ativas.
channels: Uma lista de canais disponíveis.
- `motd`: Mensagem do dia enviada aos clientes após a conexão.
- `command_handler`: Uma instância de CommandHandler para lidar com comandos.
- `logger`: Uma instância de Logger para logging.

**Métodos:**
- `__init__(self, motd, port, enable_log, log_level)`: Inicializa o servidor com os parâmetros fornecidos.
- `client_thread_loop(self, connection)`: Loop principal para lidar com mensagens dos clientes.
- `listen(self)`: Inicia o servidor e escuta por conexões.
- `message_handler(self, connection, message)`: Lida com diferentes comandos IRC.
- `disconnect_user(self, user, connection)`: Desconecta um usuário e limpa os recursos.
- `is_nickname_free(self, nickname)`: Verifica se um apelido já está em uso.
- `find_channel_by_name(self, channel_name)`: Encontra um canal pelo nome.
- `close_connection(self, user)`: Fecha a conexão para um usuário.
- `__format_out_log(self, msg)`: Formata mensagens de log para saída.
- `start(self)`: Inicia o servidor.

#### 3.1.2 `connection.py`
A classe `Connection` representa uma conexão de cliente com o servidor IRC. Ela é responsável por gerenciar a comunicação entre o cliente e o servidor, incluindo o envio e recebimento de dados e o processamento de mensagens.

**Atributos:**
- `__server`: Referência ao servidor principal.
- `is_closed`: Flag booleano indicando se a conexão está fechada.
- `socket`: O objeto socket para a conexão.
- `addr`: O endereço do cliente.
- `host`: O nome do host da conexão.
- `buffer`: Um bytearray que armazena os dados recebidos, mas ainda não processados.
- `message_history`: Uma lista de mensagens processadas (`ProcessedMessage`).
- `user`: O usuário associado à conexão.

**Métodos:**
- `__init__(self, socket: socket, addr, server)`: Inicializa a conexão com o socket, endereço e servidor fornecidos.
- `send_data(self, data: bytes)`: Envia dados ao cliente através do socket.
- `wait_for_message(self) -> ProcessedMessage`: Espera por uma mensagem do cliente, processa os dados recebidos e retorna uma instância de `ProcessedMessage`.
- `close(self)`: Fecha a conexão e remove o usuário de todos os canais.
- `parse_received_data(self)`: Processa os dados recebidos e extrai o comando e os parâmetros.

#### 3.1.3 `command_handler.py`

A classe `CommandHandler` é responsável por processar os comandos recebidos dos clientes e gerar as mensagens apropriadas para serem enviadas de volta. Ela interage com outras partes do servidor para gerenciar usuários, canais e mensagens.

**Atributos:**
- `__server`: Referência ao servidor principal.

**Métodos:**
- `__init__(self, server)`: Inicializa o manipulador de comandos com a referência ao servidor.
- `nick(self, nickname: bytearray, connection: Connection) -> List[MessageToSend]`: Processa o comando NICK para definir ou mudar o apelido do usuário.
- `user(self, username: bytearray, connection: Connection) -> List[MessageToSend]`: Processa o comando USER para definir o nome de usuário.
- `ping(self, payload: bytearray, connection: Connection) -> List[MessageToSend]`: Processa o comando PING e retorna uma resposta PONG.
- `join(self, channel_name: bytearray, connection: Connection)`: Processa o comando JOIN para adicionar um usuário a um canal.
- `privmsg(self, channel_name: bytearray, user_msg: bytearray, connection: Connection)`: Processa o comando PRIVMSG para enviar uma mensagem privada a um canal.
- `part(self, channel_name: bytearray, connection, reason: bytearray = bytearray())`: Processa o comando PART para remover um usuário de um canal.
- `names(self, channel_name: bytearray, connection)`: Processa o comando NAMES para listar os usuários de um canal.
- `quit(self, connection, reason: bytearray = bytearray())`: Processa o comando QUIT para desconectar um usuário do servidor.

**Métodos Privados:**
- `__generate_messages_for_registration(self, socket: socket, nickname: bytearray, host: bytearray, motd: bytearray) -> List[MessageToSend]`: Gera mensagens de boas-vindas e MOTD (mensagem do dia) para um usuário registrado.
- `__generate_messages_for_channel_join(self, user: User, host: bytearray, channel: Channel) -> List[MessageToSend]`: Gera mensagens para notificar sobre um novo usuário que se juntou a um canal.
- `__generate_messages_to_send_list_for_channel_join(self, user: User, channel: Channel, message_join: bytearray, message_list: bytearray, message_list_end: bytearray)`: Gera uma lista de mensagens para enviar aos usuários de um canal quando um novo usuário se junta.

### 3.2 Modulo Client

## 4. Exemplos de Uso

**Iniciando o Servidor**
```sh
python3 src/_server.py
```

**Iniciando o Client**
```sh
python3 src/_client.py
```

**Conectando ao Servidor**
* Dentro do terminal do client, utilize o seguinte comando:
```sh 
/connect <server-ip> 6667
```

```python
17:24 -!- Welcome to the Internet Relay Network novo_nick
17:24 -!- [server] - 127.0.0.1 Message of the Day -
17:24 -!- [server] - Here we love overengeneering and unnecessary complexity 
          leading to bad code!
17:24 -!- [server] End of /MOTD command.
```

**Comandos Comuns:**

* Alterar apelido: 
```
/nick <novo_apelido>
```

```
17:26 -!- You're now known as jeremias
```

* Entrar em um canal: 
```
/join #nome_do_canal
```
```
17:29 -!- jeremias [] has joined #trabalho_rc
17:29 [Users #trabalho_rc]
17:29 [ jeremias] 
17:29 -!- Irssi: #trabalho_rc: Total of 1 nicks [0 ops, 0 halfops, 0 voices, 1 
          normal]
```

* Enviar uma mensagem: 
```
/msg #nome_do_canal mensagem
```

```
17:29 -!- jeremias [] has joined #trabalho_rc
17:29 [Users #trabalho_rc]
17:29 [ jeremias] 
17:29 -!- Irssi: #trabalho_rc: Total of 1 nicks [0 ops, 0 halfops, 0 voices, 1 
          normal]
17:30 < jeremias> Ola mundo!
```

* Listar usuários em um canal: 
```
/list #nome_do_canal
```

* Sair de um canal: 
```
/leave #nome_do_canal
```

* Sair do servidor: 
```
/quit :motivo
```

## 5. Tratamento de Erros
A aplicação usa classes de erro personalizadas definidas em `errors.py` para lidar com vários erros, como apelidos inválidos, problemas de conexão e erros de canal. Esses erros são registrados adequadamente e mensagens são enviadas aos clientes para informá-los sobre os erros.

## 6. Logging
A aplicação usa uma classe `Logger` personalizada para lidar com logging. Ela registra mensagens com diferentes níveis de severidade (INFO, DEBUG, ERROR) e pode registrar mensagens coloridas para melhor legibilidade.

