import socket

# TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# endereço do servidor local de gerenciamento do microcontrolador
local_server_address = ('localhost', 10000)
print('Conectando ao servidor %s na porta %s' % local_server_address)

# conecta ao servidor de gerenciamento local
sock.connect(local_server_address)

try:
    # Send data
    message = b'Mensagem a ser transmitida'
    print('Enviando mensagem: %s' % message)
    sock.sendall(message)

    # recupera mensagens que o server esta mandando
    data = sock.recv(10)
    
    while len(data) > 0:
        #amount_received += len(data)
        print('recebido "%s"' % data)

finally:
    print('Encerrando conexão')
    sock.close()