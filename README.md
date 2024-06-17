# Trabalho Redes de Computadores - 2024/01

## 1. Visão geral
**Nome do Projeto:** Internet Relay Chat (IRC)

**Descrição:** Este projeto é uma implementação de um servidor IRC que permite aos usuarios se conectarem em canais e se cmunicarem usando vários comandos.

## 2. Modulos

### 2.1 Modulo Server

#### 2.1.1 `server.py`
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

#### 2.1.2 `connection.py`
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

#### 2.1.3 `command_handler.py`

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

#### 2.1.4 `user.py`

A classe `User` representa um usuário conectado ao servidor IRC. Ela armazena informações sobre o usuário, incluindo seu apelido, nome de usuário e os canais aos quais ele está conectado. Também fornece métodos para validar e definir apelidos e gerenciar a participação do usuário em canais.

**Atributos:**
- `nickname`: Apelido atual do usuário.
- `normalized_nickname`: Apelido normalizado do usuário (em minúsculas).
- `username`: Nome de usuário.
- `normalized_username`: Nome de usuário normalizado (em minúsculas).
- `registered`: Indica se o usuário está registrado (possui apelido e nome de usuário).
- `channels`: Lista de canais aos quais o usuário está conectado.
- `connection_socket`: Socket de conexão do usuário.
- `configuration`: Configuração do usuário, incluindo o tamanho máximo do apelido.
- `history`: Histórico de apelidos usados pelo usuário.

**Classes Internas:**
- `UserConfig`: Classe para armazenar configurações do usuário, como o tamanho máximo do apelido.
- `UserHistory`: Classe para armazenar o histórico de apelidos do usuário.

**Métodos:**
- `__init__(self, connection_socket: socket, nickname_max_size=9)`: Inicializa um novo usuário com o socket de conexão e o tamanho máximo do apelido.
- `quit_all_channels(self)`: Remove o usuário de todos os canais aos quais ele está conectado.
- `set_nickname(self, nickname: bytearray)`: Define o apelido do usuário e atualiza o apelido normalizado.
- `is_valid_nickname(self, nickname: bytearray) -> bool`: Verifica se um apelido é válido (começa com uma letra, possui tamanho adequado e contém apenas caracteres alfanuméricos ou sublinhados).
- `is_first_nick(self) -> bool`: Verifica se o apelido atual é o primeiro usado pelo usuário.
- `is_registered(self) -> bool`: Verifica se o usuário está registrado (possui apelido e nome de usuário).
- `__is_only_alphanum_or_underline(self, nickname_without_first_letter: str) -> bool`: Verifica se uma string contém apenas caracteres alfanuméricos ou sublinhados (sem contar a primeira letra).

### 2.2 Modulo Client
#### 2.2.1 `client.py`

A classe `Client` representa um cliente que se conecta a um servidor IRC. Ele é responsável por gerenciar a conexão com o servidor, manipular a entrada do usuário e receber mensagens do servidor.

**Atributos:**
- `connected`: Indica se o cliente está conectado ao servidor.
- `host`: Endereço do host ao qual o cliente está conectado.
- `port`: Número da porta à qual o cliente está conectado.
- `server_socket`: Socket usado para a conexão com o servidor.
- `ping_socket`: Socket usado para enviar pings ao servidor (não implementado).
- `logger`: Instância de Logger para logging.
- `user`: Instância de User representando o usuário do cliente.
- `input_handler`: Instância de InputHandler para manipulação da entrada do usuário.
- `message_receiver`: Instância de MessageReceiver para receber mensagens do servidor.

**Métodos:**
- `__init__(self, ip="")`: Inicializa o cliente com o endereço IP fornecido (opcional) e configura os atributos necessários.
- `connect_to_server(self, server_addr: Tuple[str, int])`: Conecta o cliente ao servidor usando o endereço e a porta fornecidos.
- `start(self)`: Inicia o cliente, incluindo o envio de pings ao servidor e a escuta de comandos de entrada do usuário.
- `input_listener_thread(self)`: Inicia a escuta de comandos de entrada do usuário.
- `server_listener_thread(self)`: Inicia a escuta de mensagens do servidor.
- `ping_sender_thread(self)`: Método reservado para enviar pings ao servidor (não implementado).

#### 2.2.2 `command_handler.py`

A classe `CommandHandler` é responsável por gerenciar os comandos enviados pelo cliente. Ela processa os comandos e envia as mensagens apropriadas ao servidor IRC.

**Atributos:**
- `client`: Instância do cliente que está conectado ao servidor.
- `user`: Instância de User representando o usuário do cliente.
- `logger`: Instância de Logger para logging.

**Métodos:**
- `__init__(self, client, user, logger)`: Inicializa o manipulador de comandos com o cliente, usuário e logger fornecidos.
- `help(self)`: Lista todos os comandos disponíveis com uma breve descrição de cada um.
- `connect(self, addr)`: Conecta o cliente ao servidor usando o endereço fornecido.
- `nick(self, nickname: str)`: Altera o apelido do usuário.
- `list(self, channel_name: str = None)`: Lista os usuários em um canal.
- `msg(self, msg: str, channel_name: str = None)`: Envia uma mensagem para um canal.
- `channel(self, channel_name: str = None)`: Seleciona um canal padrão.
- `disconnect(self, reason: str = None)`: Desconecta o cliente do servidor com uma razão opcional.
- `quit(self, reason: str)`: Sai do cliente e fecha a conexão.
- `leave(self, channel_name: str, reason: str = None)`: Sai de um canal com uma razão opcional.
- `join(self, channel_name: str)`: Entra em um canal.
- `print_msg(self, nickname: str, channel_name: str, msg: str)`: Imprime uma mensagem formatada no console.

**Métodos Privados:**
- `__format_privmsg_msg(self, channel_name: str, msg: str)`: Formata uma mensagem PRIVMSG.
- `__format_part_msg(self, channel_name, reason: str = None)`: Formata uma mensagem PART.
- `__format_nick_msg(self)`: Formata uma mensagem NICK.
- `__format_join_msg(self, channel_name: str)`: Formata uma mensagem JOIN.
- `__format_user_msg(self)`: Formata uma mensagem USER.
- `__format_registration_msg(self)`: Formata uma mensagem de registro combinando NICK e USER.
- `__format_names_msg(self, channel_name: str)`: Formata uma mensagem NAMES.
- `__format_quit_msg(self, reason: str = None)`: Formata uma mensagem QUIT.
- `__send_to_server(self, msg)`: Envia uma mensagem formatada ao servidor.

### 2.2.3 `user.py`

A classe `User` gerencia informações relacionadas ao usuário do cliente IRC, incluindo seu apelido, nome de usuário, canais que ele está participando e histórico de apelidos.

**Atributos:**
- `nickname`: Apelido atual do usuário.
- `username`: Nome de usuário do cliente.
- `registered`: Indica se o usuário está registrado no servidor.
- `channels`: Lista de canais em que o usuário está participando.
- `default_channel`: Canal padrão do usuário.
- `configuration`: Instância de `UserConfig` que armazena a configuração do usuário.
- `history`: Instância de `UserHistory` que armazena o histórico de apelidos do usuário.

**Métodos:**
- `__init__(self, nickname_max_size=9)`: Inicializa o usuário com um tamanho máximo de apelido padrão de 9 caracteres.
- `join_channel(self, channel)`: Adiciona o usuário a um canal e define o canal como padrão se ele ainda não estiver em nenhum canal.
- `quit_all_channels(self)`: Remove o usuário de todos os canais.
- `set_nickname(self, nickname: str)`: Define o apelido do usuário, adicionando o apelido atual ao histórico.
- `is_registered(self) -> bool`: Verifica se o usuário está registrado.
- `is_first_nick(self) -> bool`: Verifica se o apelido atual é o primeiro apelido do usuário.

**Métodos Privados:**
- `__is_valid_nickname(self, nickname: str) -> bool`: Verifica se o apelido é válido com base em critérios como tamanho e caracteres permitidos.
- `__is_not_in_any_channel(self)`: Verifica se o usuário não está em nenhum canal.
- `__is_only_alphanum_or_underline(self, nickname_without_first_letter: str) -> bool`: Verifica se os caracteres do apelido são alfanuméricos ou sublinhados.

## 3. Exemplos de Uso

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

## 4. Tratamento de Erros
A aplicação usa classes de erro personalizadas definidas em `errors.py` para lidar com vários erros, como apelidos inválidos, problemas de conexão e erros de canal. Esses erros são registrados adequadamente e mensagens são enviadas aos clientes para informá-los sobre os erros.

## 5. Logging
A aplicação usa uma classe `Logger` personalizada para lidar com logging. Ela registra mensagens com diferentes níveis de severidade (INFO, DEBUG, ERROR) e pode registrar mensagens coloridas para melhor legibilidade.

