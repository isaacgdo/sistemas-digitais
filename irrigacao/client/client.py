import socket
import time

# TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# endereço do servidor local de gerenciamento do microcontrolador
local_server_address = ('localhost', 10000)
print('Conectando ao servidor %s na porta %s' % local_server_address)

# conecta ao servidor de gerenciamento local
sock.connect(local_server_address)

# Função de exibição de ajuda
def listHelp():
    print("help \t \t \t- Exibe esta tela de ajuda.")
    print("start \t \t \t- começa a ler os dados do sendor de umidade.")
    print("status \t \t \t- Exibe o valor atual de leitura do sensor de umidade e da porcentagem da saída PWM da bomba.")
    print("realtime [tempo] \t- Exibe os valores do comando status em tempo real por determinado tempo informado.")
    print("settime [tempo] \t- Define de quanto em quanto tempo a bomba será acionada de acordo com o valor do sensor de umidade.")
    print("sethumidity \t \t- ")
    print("stop \t \t \t- Encerra leitura dos dados do sensor de umidade.")
    print("quit \t \t \t- Sair do programa e encerrar conexão com o servidor.")

# Caso o comando digitado não possa ser executado
def actionFail():
    print("Você não pode utilizar esse comando nesse momento.")

# Função que inicia o monitoramento
def start():
    message = b'start'
    print('Enviando mensagem: %s' % message.decode("utf-8"))
    sock.sendall(message)
    
    data = sock.recv(10)
    if len(data) > 0:
        if (data == b'failed'):
            actionFail()
        else:
            print('Iniciando monitoramento.')

# Função que mostra os estados atuais de leitura e saída
def status():
    message = b'status'
    print('Enviando mensagem: %s' % message.decode("utf-8"))
    sock.sendall(message)

    # recupera mensagens que o server esta mandando
    data = sock.recv(10)
    if len(data) > 0:
        if(data == b'failed'):
            actionFail()
        else:
            print('Valor sensor de umidade (Analógico): ',
                int(data.decode("ascii","ignore"))*4, 
                ' Valor PWM na bomba: ',
                int((int(data.decode("ascii","ignore"))/255)*100),
                '%.')


# Função de listagem de monitoramento em tempo real
def realtime(action, t):
    message = action.encode('utf-8')
    print('Enviando mensagem: %s' % action)
    sock.sendall(message)

    t_end = time.time() + t
    while time.time() < t_end:
        # recupera mensagens que o server esta mandando
        data = sock.recv(10)
        if len(data) > 0:
            if(data == b'failed'):
                actionFail()
                break
            else:
                print('Valor sensor de umidade (Analógico): ',
                    int(data.decode("ascii","ignore"))*4, 
                    ' Valor PWM na bomba: ',
                    int((int(data.decode("ascii","ignore"))/255)*100),
                    '%.')
        time.sleep(1);

def settime():
    print("action")

def sethumidity():
    print("action")
            

# Função que finaliza o monitoramento
def stop():
    message = b'stop'
    print('Enviando mensagem: %s' % message.decode("utf-8"))
    sock.sendall(message)
    # recupera mensagens que o server esta mandando
    data = sock.recv(10)
    if len(data) > 0:
        if(data == b'failed'):
            actionFail()
        else:
            print('Encerrando monitoramento.')

def quit():
    message = b'quit'
    print('Enviando mensagem: %s' % message.decode("utf-8"))
    sock.sendall(message)

try:
    running = True
    print("Bem-vindo ao servidor de monitoramento e controle de irrigação automático.")
    print("Insira um comando. Em caso de dúvidas, insira o comando 'help'.")

    while(running == True):
        action = input('Comando: ')
        if (action == 'help'):
            listHelp()
        elif (action == 'start'):
            start()
        elif (action == 'status'):
            status()
        elif (action[0:8] == 'realtime'):
            splitted = action.split(' ')
            realtime(action, int(splitted[1]))
        elif (action == 'stop'):
            stop()    
        elif (action == 'quit'):
            quit()
            running = False
        else:
            print("Comando inválido.")
finally:
    print('Encerrando conexão.')
    sock.close()
