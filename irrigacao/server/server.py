import socket
import serial
import time

# TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connection serial setting
serial_connection = serial.Serial('/dev/ttyUSB0',9600)

# endereço do servidor local de gerenciamento do microcontrolador
local_server_address = ('localhost', 10000)
sock.bind(local_server_address)
print('Servidor %s rodando na porta %s' % local_server_address)

# Permite o socket escutar conexões
sock.listen(True)

def start():
    serial_connection.write(b'1')

def status():
    # = int(serial_connection.readline(10).decode("ascii","ignore"))
    serial_connection.flush()
    output = serial_connection.readline()
    serial_connection.write(b'2')
    return output

def settime(t):
    serial_connection.flush()
    output = serial_connection.readline()
    print("settime function liftoff!")
    serial_connection.write(bytes(t, 'ascii'))

def stop():
    serial_connection.write(b'3')

# Loop de conexão cliente-servidor
while True:
    print('Aguardando uma conexão...')
    connection, client_address = sock.accept()  # Aguarda conexão
    print('Conexão feita por: ', client_address)

    try:
        lastCommand = 'stop'
        # Loop de recepção de mensagens do cliente remoto
        while True:
            data = connection.recv(16)  # Aguarda comandos

            #Loop de controle dos comandos passados
            while True:
                print('recebido: %s' % data.decode("utf-8"))
                if data != '' and lastCommand != "quit":
                    if (data == b'start' and lastCommand == "stop"):
                        start()
                        connection.sendall(data)
                        lastCommand = "start"
                        break
                    elif (data == b'status' and 
                            (lastCommand == "start" or 
                            lastCommand == "status" or 
                            lastCommand == "realtime" or
                            lastCommand == "settime")):
                    
                        connection.sendall(status())
                        lastCommand = "status"
                        break
                    elif (data.decode('utf-8')[0:8] == 'realtime' and
                            (lastCommand == "start" or 
                            lastCommand == "status" or 
                            lastCommand == "realtime" or
                            lastCommand == "settime")):

                        splitted = data.decode('utf-8').split(' ')
                        t_end = time.time() + int(splitted[1])
                        lastCommand = "realtime"
                        while time.time() < t_end:
                            connection.sendall(status())
                            time.sleep(1);
                        break
                    elif (data.decode('utf-8')[0:7] == 'settime' and 
                            (lastCommand == "start" or 
                            lastCommand == "status" or 
                            lastCommand == "realtime" or
                            lastCommand == "settime")):

                        splitted = data.decode('utf-8').split(' ')
                        settime(splitted[1])
                        connection.sendall(data)
                        lastCommand = "settime"
                        break
                    elif (data == b'stop' and lastCommand != "stop"):
                        stop()
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
    # except:
    #     print("Falha ao receber o comando.")

    finally:
        # Encerra conexão
        connection.close()
