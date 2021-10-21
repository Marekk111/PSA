#!/usr/bin/env python3

import socket

ADRESS = "127.0.0.1"
PORT = 9999

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ADRESS, PORT))
    sprava = input("Zadaj spravu: ")
    sock.send(sprava.encode())
