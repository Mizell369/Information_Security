#!/usr/bin/python3
import socket
#soc = socket.socket()
#ip = input("Please enter the IP: ")
#port = str(input("Please enter the port no: "))
#soc.connect((ip,int(port)))
#print(soc.recv(1024))

def banner(ip, port):
    soc = socket.socket()
    soc.connect((ip, int(port)))
    soc.settimeout(5)
    #print(soc.recv(1024))
    print(str(soc.recv(1024)).strip("b'"))

def main():
    ip = input("Please enter the IP: ")
    port = str(input("Please enter the Port: "))
    banner(ip, port)

main()
    