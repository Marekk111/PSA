#!/usr/bin/env python3
from scapy.all import *
import struct


def macDoBajtov(paMAC):   
    # zo stringu odstranim dvojbodky, HEX string premenim na bajty 
    return bytes.fromhex(paMAC.replace(":", ""))

def nastavBit(paVstup, paBit):
    return paVstup | (1<<(paBit-1))

class EthRamec():
    def __init__(self, paSRCMAC):
        self.aDSTMAC = "01:00:0C:CC:CC:CC"
        self.aSRCMAC = paSRCMAC
        self.aLength = 0
    
    def pridajPayload(self, paPayload):
        self.aPayload = paPayload

    def dajBajty(self):
        telo = self.aPayload.dajBajty()
        self.aLength = len(telo)
        return (macDoBajtov(self.aDSTMAC)
                + macDoBajtov(self.aSRCMAC) 
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

    def dajBajty(self):
        return (struct.pack("!3B", self.aDSAP, self.aSSAP, self.aCTRL)
                + macDoBajtov(self.aOUI)
                + struct.pack("!H", self.aPID)
                + self.aPayload.dajBajty()
               )

class CDP():
    def __init__(self):
        self.aVersion = 1
        self.aTTL = 180
        self.aChecksum = 0x0000
        self.aTLVs = list()

    def pridajTLV(self, paTLV):
        self.aTLVs.append(paTLV)

    def dajBajty(self):
        bajty = struct.pack("!2BH", 
                            self.aVersion,
                            self.aTTL,
                            self.aChecksum)
        for tlv in self.aTLVs:
            bajty += tlv.dajBajty()
        # TODO: vypocitat checksum z bajty
        # TODO: nahradit checksum v bajty
        return bajty

class TLV():
    def __init__(self, paTyp):
        self.aType = paTyp
        self.aLength = 4

    def dajBajty(self):
        return struct.pack("!2H", self.aType, self.aLength)

class TLVDeviceID(TLV):
    def __init__(self, paDeviceID):
        TLV.__init__(self, 0x0001)
        self.aDeviceID = paDeviceID

    def dajBajty(self):
        idbajty = self.aDeviceID.encode()
        self.aLength += len(idbajty)
        return TLV.dajBajty(self) + idbajty

class TLVSoftware(TLVDeviceID):
    def __init__(self, paSoftware):
        super().__init__(paSoftware)
        self.aType = 0x0005

class TLVPlatform(TLVDeviceID):
    def __init__(self):
        super().__init__("Python3")
        self.aType = 0x0006

class TLVCapabilities(TLV):
    def __init__(self, paRouter=False, paSwitch=False, paHost=False, paPhone=False):
        TLV.__init__(self, 0x0004)
        self.aRouter = paRouter
        self.aSwitch = paSwitch
        self.aHost = paHost
        self.aPhone = paPhone
        self.aCapabilities = 0x00000000

    def dajBajty(self):
        self.aLength += 4

        if self.aRouter:
            self.aCapabilities = nastavBit(self.aCapabilities, 1)
            #self.aCapabilities += 1
        if self.aSwitch:
            self.aCapabilities += 8 #4ty bit
        if self.aHost:
            self.aCapabilities = nastavBit(self.aCapabilities, 5)
        if self.aPhone:
            self.aCapabilities = nastavBit(self.aCapabilities, 8)
      
        return super().dajBajty() + struct.pack("!I", self.aCapabilities)
    
if __name__ == "__main__":
    IFACES.show()
    # rozhranie podla nazvu
    # rozhranie = "Software Loopback Interface 1"
    rozhranie = IFACES.dev_from_index(16)
    sock = conf.L2socket(iface=rozhranie)

    cdp = CDP()
    cdp.pridajTLV(TLVDeviceID("Rychlejsi pocitac"))
    cdp.pridajTLV(TLVPlatform())
    cdp.pridajTLV(TLVSoftware("Windows 10 x64 20H2"))
    cdp.pridajTLV(TLVCapabilities(True, True, True, True))
    
    llc = Llc()
    llc.pridajPayload(cdp)

    ramec = EthRamec("01:02:03:04:05:06")
    ramec.pridajPayload(llc)

    sock.send(ramec.dajBajty())