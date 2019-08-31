import socket
import serial

# TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# endereço do servidor local de gerenciamento do microcontrolador
local_server_address = ('localhost', 10000)
print('Servidor %s rodando na porta %s' % local_server_address)
sock.bind(local_server_address)

# Permite o socket escutar conexões
sock.listen(True)

def controllerFlag():
    # connection serial setting
    serial_connection = serial.Serial('/dev/ttyACM0',9600)

    while True:
        output= int(serial_connection.readline(10))
        if(output>20 and output<85):
            serial_connection.write(b'1')
        elif(output>=85 and output<170):
            serial_connection.write(b'2')
        elif(output>=170 and output<255):
            serial_connection.write(b'3')
        else:
            serial_connection.write(b'0')
        print(output)
        output=0

# Loop de conexão cliente-servidor
while True:
    print('Aguardando uma conexão...')
    connection, client_address = sock.accept()  # Aguarda conexão
    print('Conexão feita por: ', client_address)

    try:
        lastCommand = 'stop'
        # Loop de recepção de mensagens do cliente remoto
        while True:
            data = connection.recv(10)  # Aguarda comandos    //TODO erro de releitura

            #Loop de controle dos comandos passados
            while True:
                print('recebido: %s' % data.decode("utf-8"))
                if data != '' and lastCommand != "quit":
                    if (data == b'start' and lastCommand != "start"):
                        print('Enviando dados de volta para o cliente.')
                        #controllerFlag()
                        connection.sendall(data)
                        lastCommand = "start"
                        break
                    elif (data == b'status' and (lastCommand == "start" or lastCommand == "status")):
                        print("status")
                        connection.sendall(data)
                        lastCommand = "status"
                        break
                    elif (data == b'stop' and lastCommand != "stop"):
                        print('Encerrando monitoramento.')
                        connection.sendall(data)
                        lastCommand = "stop"
                        break
                    elif (data == b'quit'):
                        connection.close()
                        lastCommand = "quit"
                        break
                    else:
                        connection.sendall(b'failed')
                        break
            if lastCommand == "quit":
                break
    except:
        print("Falha ao receber o comando.")

    finally:
        # Encerra conexão
        connection.close()
