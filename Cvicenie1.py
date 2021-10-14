#!/usr/bin/env python
class Pozdrav:
    def __init__(self, pMeno):
        self.aMeno = pMeno
        self.aPozdravEN = ("Hello")
        self.aPozdravSK = ("Ahoj")
    
    def pozdravMna(self, paJazyk):
        if paJazyk == "EN":
            return self.aPozdravEN + " " + self.aMeno
        if paJazyk == "SK":
            return self.aPozdravSK + " " + self.aMeno
        else:
            return "Zly input!" 

jazyk = input("Zadaj jazyk: ")
meno = input("Zadaj meno: ")

hello = Pozdrav(meno)
print(hello.pozdravMna(jazyk))

