from hashlib import sha256
from .block import Block
import time
import json
from django.core.serializers.json import DjangoJSONEncoder

class Blockchain:

    # PreviousHash setado para ser utilizado apenas no bloco genesis
    genesisPreviousHash = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        # "Profundidade" da blockchain
        self.deep = 0
        # Lista de blocos (A blockchain)
        self.chain = []
        # Dificuldade da mineração de novos blocos
        self.difficulty = 3

    def addBlock(self, data):

        # Caso a blockchain esteja vazia
        if(self.deep==0):
            # Cria o bloco genesis
            self.createGenesisBlock((data))

        # Caso a blockchain não esteja vazia
        else:
            # Adiciona o novo bloco, passando seus dados, o hash do bloco anterior e o índice do novo bloco
            self.chain.append(Block(data, self.chain[self.deep-1].myHash, self.deep))
            self.deep+=1

    def createGenesisBlock(self, data):
        # Adiciona o bloco, passando seus dados, o previousHash setado e o índice do bloco
        self.chain.append(Block(data, self.genesisPreviousHash, self.deep))
        self.deep+=1

    def showBlocks(self):
        for block in self.chain:
            block.showFullData()

    def isChainValid(self):

        # Construindo uma string de zeros do tamanho da dificuldade da blockchain
        target = "0"*self.difficulty

        # Para todos os blocos da blockchain
        for currentBlock in self.chain:

            # Se não houverem blocos, não é válida
            if(self.deep==0):
                return False

            # Hash correto do bloco
            realHash = sha256(currentBlock.getAttributesAsString().encode()).hexdigest()

            # Caso Geral:
            #   Caso o hash do bloco seja diferente do que deveria ser
            #   Ou
            #   Caso o hash do bloco não tenha sido validado pelo PoW
            if(currentBlock.myHash != realHash or
                currentBlock.myHash[:self.difficulty] != target):
                return False

            # Caso específico do bloco genesis:
            if(currentBlock.index==0):
                if(currentBlock.previousHash != self.genesisPreviousHash):
                    return False
            # Caso específico dos outros blocos:
            else:
                previousBlock = self.chain[currentBlock.index-1]
                # Caso o previousHash do bloco atual seja diferente do hash do bloco anterior
                if(currentBlock.previousHash != previousBlock.myHash):
                    return False

        return True



    def proofOfWork(self, index, difficulty):

        # Construindo uma string de zeros do tamanho da dificuldade da blockchain
        target = "0"*difficulty

        # Enquanto os 'n = difficulty' primeiros caracteres do hash atual não forem iguais a zero,
        # incrementar o nonce e recalcular o hash
        while(self.chain[index].myHash[:difficulty] != target):
            self.chain[index].nonce+=1
            self.chain[index].setHash()


    def validateChain(self):

        start = time.time()

        # Construindo uma string de zeros do tamanho da dificuldade da blockchain
        target = "0"*self.difficulty

        for block in self.chain:

            blockStart = time.time()

            # Caso seja o bloco genesis e seu previousHash
            # seja diferente do que deveria ser, ajustá-lo
            if(block.index==0):
                if(block.previousHash != self.genesisPreviousHash):
                    self.chain[block.index].previousHash = self.genesisPreviousHash
                    self.proofOfWork(block.index, self.difficulty)

            # Caso não seja o bloco genesis, comparar o previousHash
            # do bloco atual com o hash do bloco anterior, ajustá-lo
            elif(block.previousHash != self.chain[block.index-1].myHash):
                self.chain[block.index].previousHash = self.chain[block.index-1].myHash
                self.proofOfWork(block.index, self.difficulty)

            # Hash correto do bloco atual
            realHash = sha256(block.getAttributesAsString().encode()).hexdigest()

            # Caso o bloco não tenha sido validado pelo
            # PoW, fazer a validação
            # Ou
            # Caso o hash do bloco atual seja diferente
            # do que realmente deveria ser
            if(block.myHash != realHash or block.myHash[:self.difficulty] != target):
                self.proofOfWork(block.index, self.difficulty)

            print("Validação de " + block.data + " demorou " + str(time.time() - blockStart) + " segundos.")

        print("\nTempo total: " + str(time.time() - start) + " segundos.")

def main():
    c = Blockchain()

    c.addBlock("Petr Cech")
    c.addBlock("Branislav Ivanovic")
    c.addBlock("Ricardo Carvalho")
    c.addBlock("John Terry")
    c.addBlock("Ashley Cole")
    c.addBlock("N'Golo Kanté")
    c.addBlock("Cesc Fàbregas")
    c.addBlock("Frank Lampard")
    c.addBlock("Eden Hazard")
    c.addBlock("Juan Mata")
    c.addBlock("Didier Drogba")

    print("A cadeia é válida!\n" if c.isChainValid() else "A cadeia é inválida!\n")
    c.showBlocks()
    c.validateChain()
    c.showBlocks()
    print("A cadeia é válida!\n" if c.isChainValid() else "A cadeia é inválida!\n")
    return c.chain
"""
    for bloco in c.chain:
        print(json.dumps(bloco.getAttributesTypes(), cls=DjangoJSONEncoder))
    print(json.dumps(Usuario.objects.all()))

    print(json.dumps(c.chain, indent=4, sort_keys=True, cls=DjangoJSONEncoder), )
    with open("teste.json", "w") as write_file:
        for bloco in c.chain:
            json.dump(bloco, write_file, indent=4, sort_keys=True, cls=DjangoJSONEncoder)
"""

if __name__ == "__main__":
    main()

# https://medium.com/@raul_11817/rsa-with-cryptography-python-library-462b26ce4120
# https://docs.python.org/3/library/base64.html#module-base64
# https://stackoverflow.com/questions/45146504/python-cryptography-module-save-load-rsa-keys-to-from-file
