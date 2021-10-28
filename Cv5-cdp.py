#!usr/bin/env python3
from scapy.all import *

class EthRamec():
    def __init__(self, paSRCMAC):
        self.aDSTMAC = "01:00:0C:CC:CC:CC"
        self.aSRCMAC = paSRCMAC
        self.aLength = 0

    def pridajPayload(self, paPayload):
        self.aPayload = paPayload
    
    def dajByty(self):
        

if __name__ == "__main__":
    IFACES.show()
    
    #rozhranie podla nazvu
    #rozhranie = "Software Loopback Interface 1"
    
    #rozhranie podla indexu
    rozhranie = IFACES.dev_from_index(1)
    sock = conf.L2socket(iface=rozhranie)
    sock.send("Ahoj".encode())
