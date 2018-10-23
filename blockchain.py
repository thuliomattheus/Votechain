from block import Block
from hashlib import sha256

class Blockchain:

    genesisPreviousHash = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self.deep = 0
        self.chain = []
        self.difficulty = 5

    def addBlock(self, newBlockData):
        if(self.deep==0):
            self.createGenesisBlock((newBlockData))
        else:
            self.chain.append(Block(newBlockData, self.chain[self.deep-1].hash, self.deep))
            self.deep+=1

    def createGenesisBlock(self, newBlockData):
        self.chain.append(Block(newBlockData, self.genesisPreviousHash, self.deep))
        self.deep+=1

    def showBlocks(self):
        for b in self.chain:
            b.showFullData()

    def isChainValid(self):

        # Construindo uma string de zeros do tamanho da dificuldade da blockchain
        target = "0"*self.difficulty

        # Para todos os blocos
        for b1 in self.chain:

            if(self.deep==0):
                return False

            aux = sha256(b1.getAttributesAsString().encode()).hexdigest()

            # Caso o hash do bloco seja diferente do que deveria ser
            # Ou
            # Caso o hash do bloco não tenha passado pelo PoW
            if(b1.hash != aux or
                b1.hash[:self.difficulty] != target):
                return False

            # Se o previousHash do bloco atual for diferente do hash do antigo bloco
            if(b1.index==0):
                if(b1.previousHash != self.genesisPreviousHash):
                    return False
            else:
                b0 = self.chain[b1.index-1]
                if(b1.previousHash != b0.hash):
                    return False

        return True



    def proofOfWork(self, index, difficulty):

        # Construindo uma string de zeros do tamanho da dificuldade da blockchain
        target = "0"*difficulty

        while(self.chain[index].hash[:difficulty] != target):
            self.chain[index].nonce+=1
            self.chain[index].setHash()


    def validateChain(self):

        # Construindo uma string de zeros do tamanho da dificuldade da blockchain
        target = "0"*self.difficulty

        for i in self.chain:

            # Caso seja o bloco genesis
            if(i.index==0):
                if(i.hash[:self.difficulty] != target):
                    self.proofOfWork(i.index, self.difficulty)

            elif(i.previousHash != self.chain[i.index-1].hash):
                i.previousHash = self.chain[i.index-1].hash
                self.proofOfWork(i.index, self.difficulty)

            elif(i.hash[:self.difficulty] != target):
                self.proofOfWork(i.index, self.difficulty)




c = Blockchain()

c.addBlock("Petr Cech")
c.addBlock("Branislav Ivanovic")
c.addBlock("Ricardo Carvalho")
c.addBlock("John Terry")
c.addBlock("Marcos Alonso")
c.addBlock("N'Golo Kanté")
c.addBlock("Cesc Fàbregas")
c.addBlock("Frank Lampard")
c.addBlock("Eden Hazard")
c.addBlock("Juan Mata")
c.addBlock("Didier Drogba")

print("A cadeia é válida!\n" if c.isChainValid() else "A cadeia é inválida!\n")
c.validateChain()
c.showBlocks()
print("A cadeia é válida!\n" if c.isChainValid() else "A cadeia é inválida!\n")

# https://medium.com/@raul_11817/rsa-with-cryptography-python-library-462b26ce4120
# https://docs.python.org/3/library/base64.html#module-base64
# https://stackoverflow.com/questions/45146504/python-cryptography-module-save-load-rsa-keys-to-from-file
