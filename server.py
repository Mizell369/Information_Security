#!/usr/bin/python3
import socket
#Creating the socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 444
#binding to socket
serversocket.bind(('192.168.1.10', 444))#host will be substituted with IP, if changed and running on host
#Starting TCP listener
serversocket.listen(3)

while True:
    #Starting the connection
    clientsocket, address = serversocket.accept()
    print("connection received from %s " % str(address))
    message = 'hello! Thank You for connecting to the server' + '\r\n'
    clientsocket.send(message.encode('ascii'))
    clientsocket.close()
