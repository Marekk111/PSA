#!/usr/bin/env python3
import socket
ADRESS = "0.0.0.0"
PORT = 9998

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ADRESS, PORT))
    sock.listen(10)

    while(True):
        (clientSock, clientAddr) = sock.accept()
        while(True):
            sprava = clientSock.recv(1500)
            print("Sprava od {}:{} {}".format(clientAddr[0], clientAddr[1], sprava))
            clientSock.close()
        