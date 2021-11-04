#!usr/bin/env python3
from scapy.all import *
import struct

def convertMAC(paMAC):
    #zmeni MAC adresu z hex cisla do bytov
    return bytes.fromhex(paMAC.replace(":", ""))

class EthRamec():
    def __init__(self, paSRCMAC):
        self.aDSTMAC = "01:00:0C:CC:CC:CC"
        self.aSRCMAC = paSRCMAC
        self.aLength = 0

    def pridajPayload(self, paPayload):
        self.aPayload = paPayload
    
    def dajByty(self):
        telo = self.aPayload
        self.aLength = len(telo)
        return (convertMAC(self.aDSTMAC) 
                + convertMAC(self.aSRCMAC) 
                + struct.pack("!H", self.aLength) 
                + telo)

class Llc():
    def __init__(self):
        self.aDSAP = 0xAA
        self.aSSAP = 0xAA
        self.aCTRL = 0x03
        self.aOUI = "00:00:0C"
        self.aPID = 0x2000
    
    def pridajPayload(self, paPayload):
        self.aPayload = paPayload
    
    def dajByty(self):
        return (struct.pack("!3B", self.aDSAP, self.aSSAP, self.aCTRL) 
                + convertMAC(self.aOUI)
                + struct.pack("!H", self.aPID)
                + self.aPayload)

class CDP():
    def __init__(self):
        self.aVersion = 1
        self.aTTL = 180
        self.aChecksum = 0x0000
        self.aTLVs = list()
    
    def pridajTLV(self, paTLV):
        self.aTLVs.append(paTLV)

    def dajByty(self):
        byty = struct.pack("!2BH", 
                            self.aVersion, 
                            self.aTTL, 
                            self.aChecksum)
        for tlv in self.aTLVs:
            tlv.dajByty()
            byty += tlv.dajByty()
        #TODO: vypocitat checksum v bajty
        #TODO: nahradit checksum v bajty
        return byty 

class TLV():
    def __init__(self, paTyp):
        self.aType = paTyp
        self.aLength = 4
    
    def dajByty(self):
        return struct.pack("!2H", self.aType, self.aLength)

if __name__ == "__main__":
    IFACES.show()
    
    #rozhranie podla nazvu
    #rozhranie = "Software Loopback Interface 1"
    
    #rozhranie podla indexu
    rozhranie = IFACES.dev_from_index(13)
    sock = conf.L2socket(iface=rozhranie)
    llc = Llc()
    llc.pridajPayload("Ahoj".encode())
    ramec = EthRamec("01:02:03:04:05:06")
    ramec.pridajPayload(llc)
    sock.send(ramec.dajByty())
