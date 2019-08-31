import serial

# connection setting
connection = serial.Serial('/dev/ttyUSB0',9600)

def controllerFlag():
    while True:
        output=int(connection.readline(10))
        if(output>=0 and output<85):
            connection.write(b'1')
        elif(output>=85 and output<170):
            connection.write(b'2')
        elif(output>=170 and output<=255):
            connection.write(b'3')
        else:
            connection.write(b'0')
        print(output)
        output=0

controllerFlag()
