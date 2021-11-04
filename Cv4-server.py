#!/usr/bin/env python3
import socket
from enum import IntEnum
import json

ADRESS = "0.0.0.0"
PORT = 9998

class Sprava:
    def __init__(self, paOd, paKomu, paOperacia, paText):
        self.aOd = paOd
        self.aKomu = paKomu
        self.aOperacia = paOperacia
        self.aText = paText
    
    @staticmethod
    def jsonParser(obj):
        return Sprava(obj['aOd'], obj['aKomu'], obj['aOperacia'], obj['aText'])
        

class Operacia(IntEnum):
    LOGIN = 1
    EXIT = 2
    USERS = 3

def handleClient(clientSock, clientAddr):
    print("Pripojil sa klient: {}:{}".format(clientAddr[0], clientAddr[1]))
    while(True):
        sprava = clientSock.recv(1500)
        print("Sprava od {}:{} {}".format(clientAddr[0], clientAddr[1], sprava.decode()))

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ADRESS, PORT))
    sock.listen(10)


    while(True):
        (clientSock, clientAddr) = sock.accept()
        vlakno = threading.Thread(target = handleClient, args=(clientSock, clientAddr))
        while(True):
            sprava = clientSock.recv(1500)
            print("Sprava od {}:{} {}".format(clientAddr[0], clientAddr[1], sprava))
            clientSock.close()
        