from datetime import datetime
from hashlib import sha256

class Block:

    def __init__(self, data, previousHash, index):

        self.nonce = 0 #int
        self.data = data #document
        self.previousHash = previousHash #string
        self.index = index #int
        self.timestamp = datetime.now().strftime("%d/%m/%y - %T") #string
        self.setHash() #hex string

    def getAttributesAsString(self):
        return (self.data + str(self.index) + self.timestamp +
                self.previousHash + str(self.nonce))

    def showFullData(self):
        print("Índice        : " + str(self.index))
        print("Timestamp     : " + self.timestamp)
        print("Dados         : " + self.data)
        print("Nonce         : " + str(self.nonce))
        print("Hash Anterior : " + self.previousHash)
        print("Hash Atual    : " + self.hash+"\n")

    def setHash(self):
        self.hash=sha256(self.getAttributesAsString().encode()).hexdigest()
