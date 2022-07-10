#!/usr/bin/python3
import socket
#Creating the socket object
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 444

clientsocket.connect(('192.168.1.10', 444))

message = clientsocket.recv(1024)

clientsocket.close()
print(message.decode('ascii'))