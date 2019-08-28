import socket
import serial

# TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# endereço do servidor local de gerenciamento do microcontrolador
local_server_address = ('localhost', 10000)
print('Servidor %s rodando na porta %s' % local_server_address)

sock.bind(local_server_address)

# Permite o socket escutar conexões
sock.listen(1)

while True:
    # Aguarda conexão
    print('Aguardando uma conexão')
    connection, client_address = sock.accept()
    try:
        print('Conexão feita por: ', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(10)
            # connection setting
            #connection = serial.Serial('/dev/ttyUSB0',9600)
            #controllerFlag();

            print('recebido "%s"' % data)
            if data:
                print('Enviando dados de volta para o cliente')
                connection.sendall(data)
            else:
                print('sem novas entradas de ', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()


def controllerFlag():
    while True:
        output= int(connection.readline(10))
        if(output>20 and output<85):
            connection.write(b'1')
        elif(output>=85 and output<170):
            connection.write(b'2')
        elif(output>=170 and output<255):
            connection.write(b'3')
        else:
            connection.write(b'0')
        print(output)
        output=0