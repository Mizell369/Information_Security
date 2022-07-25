#!/usr/bin/python3

import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = input("Please enter the IP to scan: ")
port = int(input("Please enter the port to scan: "))
soc.settimeout(5)

def portScanner(port):
    if soc.connect_ex((host,port)):
        print("The Port is closed")
    else:
        print("The Port is Open")

portScanner(port)