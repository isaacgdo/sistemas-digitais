import socket
import serial
import time
import threading

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
    output = serial_connection.readline()
    if 'stop_thread_settime' in globals():
        if stop_thread_settime == True:
            serial_connection.write(b'1')
        else:
            serial_connection.write(b'3')
            serial_connection.write(b'3')
    else:
        serial_connection.write(b'1')

    return output

def settime(t):
    splitted = t.split('-')
    # serial_connection.flush()
    output = serial_connection.readline()
    while True:
        global stop_thread_settime
        serial_connection.write(b'3')
        time.sleep(int(splitted[0]));
        serial_connection.write(b'3')
        time.sleep(int(splitted[1]));
        if stop_thread_settime == True:
            break

def stop():
    serial_connection.write(b'2')

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

            #Controle dos comandos passados
            print('recebido: %s' % data.decode("utf-8"))
            if data != '' and lastCommand != "quit":
                if (data == b'start' and lastCommand == "stop"):
                    start()
                    connection.sendall(data)
                    lastCommand = "start"
                elif (data == b'status' and 
                        (lastCommand == "start" or 
                        lastCommand == "status" or 
                        lastCommand == "realtime" or
                        lastCommand == "settime")):
                    connection.sendall(status())
                    lastCommand = "status"
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
                        time.sleep(0.5);
                elif (data.decode('utf-8')[0:7] == 'settime' and 
                        (lastCommand == "start" or 
                        lastCommand == "status" or 
                        lastCommand == "realtime" or
                        lastCommand == "settime")):

                    splitted = data.decode('utf-8').split(' ')
                    thread_settime = threading.Thread(target=settime, args=(splitted[1],))
                    thread_settime.start()
                    stop_thread_settime = False
                    # settime(splitted[1])
                    connection.sendall("settime".encode('utf-8'))
                    lastCommand = "settime"
                elif (data == b'stop' and lastCommand != "stop"):
                    stop_thread_settime = True
                    time.sleep(0.1)
                    stop()
                    connection.sendall(data)
                    lastCommand = "stop"
                elif (data == b'quit'):
                    connection.close()
                    lastCommand = "quit"
                else:
                    connection.sendall(b'failed')
            if lastCommand == "quit":
                break
    except:
        print("Falha ao receber o comando.")

    finally:
        # Encerra conexão
        connection.close()
