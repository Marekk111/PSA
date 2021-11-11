#!/usr/bin/env python3

import socket
from enum import IntEnum
import json

ADRESA = "127.0.0.1"
PORT = 9999

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

def napoveda():
    print("***Napoveda")
    print("  \q Ukonci program")
    print("  \l Vypis pouzivatelov")
    print("  \h Vypis napovedu")
    print("Spravu posielame v tvare nick;text")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ADRESA, PORT))

    print("Vita vas CHAT klient.")
    nick = input("Zadajte vas nick: ")
    napoveda()
    # prihlasenie sa na server (pre zoznam pouzivatelov)
    sprava = Sprava(nick, '', Operacia.LOGIN, '')
    jsonStr = json.dumps(sprava.__dict__)
    sock.send(jsonStr.encode())

    while(True):
        prikaz = input("Zadajte prikaz/spravu: ")

        if prikaz[0] == "\\":
            # mam specialny prikaz
            if prikaz[1] == "q":
                # ukoncujem program
                sprava = Sprava(nick, '', Operacia.EXIT, '')
                jsonStr = json.dumps(sprava.__dict__)
                sock.send(jsonStr.encode())
                sock.close()
                exit(0)
            if prikaz[1] == "h":
                napoveda()
                continue
            if prikaz[1] == "l":
                sprava = Sprava(nick, '', Operacia.USERS, '')
                jsonStr = json.dumps(sprava.__dict__)
                sock.send(jsonStr.encode())
                data = sock.recv(1500)
                sprava = json.loads(data.decode(), object_hook=Sprava.jsonParser)
                print("Zoznam pouzivatelov: " + sprava.aText)
                continue
        
        zoznam = prikaz.split(";", 1)
        sprava = Sprava(nick, zoznam[0], '', zoznam[1])
        jsonStr = json.dumps(sprava.__dict__)
        sock.send(jsonStr.encode())