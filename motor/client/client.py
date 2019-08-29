import socket

# TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# endereço do servidor local de gerenciamento do microcontrolador
local_server_address = ('localhost', 10000)
print('Conectando ao servidor %s na porta %s' % local_server_address)

# conecta ao servidor de gerenciamento local
sock.connect(local_server_address)

# Função de exibição de ajuda
def listHelp():
    print("help - Exibe esta tela de ajuda.")
    print("start - começa a ler os dados do sendor de umidade.")
    print("status - Exibe o valor atual de leitura do sensor de umidade e da porcentagem da saída PWM da bomba.")
    print("settime - ")
    print("sethumidity - ")
    print("stop - Encerra leitura dos dados do sensor de umidade.")
    print("realtime - Exibe os valores do comando status em tempo real.")
    print("quit - Sair do programa e encerrar conexão com o servidor.")

# Função que inicia o monitoramento
def start():
    message = b'start'
    print('Enviando mensagem: %s' % message.decode("utf-8"))
    sock.sendall(message)
    # recupera mensagens que o server esta mandando
    data = sock.recv(10)
    
    while True:
        if len(data) > 0:
            #amount_received += len(data)
            print('recebido: %s' % data)
            break

# Função que finaliza o monitoramento
def stop():
    message = b'stop'
    print('Enviando mensagem: %s' % message.decode("utf-8"))
    sock.sendall(message)
    # recupera mensagens que o server esta mandando
    data = sock.recv(10)
    
    while True:
        if len(data) > 0:
            #amount_received += len(data)
            print('recebido: %s' % data)
            break

def status():
    print("action")

def settime():
    print("action")

def sethumidity():
    print("action")

def realtime():
    print("action")

try:
    running = True
    print("Bem-vindo ao servidor de monitoramento e controle de irrigação automático.")
    print("Insira um comando. Em caso de dúvidas, insira o comando 'help'.")

    while(running == True):
        action = input('Comando: ')
        if (action == 'start'):
            start()
        elif (action == 'stop'):
            stop()    
        elif (action == 'quit'):
            running = False
        elif (action == 'help'):
            listHelp()
        else:
            print("Comando inválido")
finally:
    print('Encerrando conexão')
    sock.close()
