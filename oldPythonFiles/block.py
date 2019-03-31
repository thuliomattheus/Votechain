from datetime import datetime
from hashlib import sha256

class Block:

    def __init__(self, data, previousHash, index):

        self.nonce = 0 #int
        self.data = data #dict
        self.previousHash = previousHash #string
        self.index = index #int
        self.timestamp = datetime.now() #date
        self.setHash() #hex string

    def getAttributesAsString(self):
        return (self.data + str(self.index) + self.timestamp.strftime("%d/%m/%y - %T") +
                self.previousHash + str(self.nonce))

    def getAttributesTypes(self):
        return (str(type(self.nonce)) +
                str(type(self.data))+
                str(type(self.previousHash)) +
                str(type(self.index)) +
                str(type(self.timestamp)) +
                str(type(self.myHash) ))

    def showFullData(self):
        print("Índice        : " + str(self.index))
        print("Timestamp     : " + self.timestamp.strftime("%d/%m/%y - %T"))
        print("Dados         : " + self.data)
        print("Nonce         : " + str(self.nonce))
        print("Hash Anterior : " + self.previousHash)
        print("Hash Atual    : " + self.myHash+"\n")

    def setHash(self):
        self.myHash = sha256(self.getAttributesAsString().encode()).hexdigest()