from django.db import models
from hashlib import sha256
from nodeProject.nodeApp import utilities
from nodeProject.blockchainReusableApp.models import AbstractVote, AbstractSeeder

class Block(models.Model):
    index = models.PositiveIntegerField(primary_key=True, blank=False, null=False)
    timestamp = models.DateTimeField(blank=False, null=False)
    votes = models.TextField() # Json com a lista de votos
    difficulty = models.PositiveIntegerField(blank=False, null=False)
    nonce = models.BigIntegerField(blank=False, null=False, default=-1)
    previousBlockHash = models.CharField(max_length=512, blank=False, null=False)
    currentBlockHash = models.CharField(max_length=512, blank=False, null=False, default="1"*64)

    def __str__(self):
        return ("Bloco " + str(self.index))

    def getAttributesAsList(self):
        return [
                self.index,
                utilities.dateToString(self.timestamp),
                self.votes,
                self.difficulty,
                self.nonce,
                self.previousBlockHash
            ]

    def realHash(self):
        return utilities.encryptSha256(utilities.concatenate(self.getAttributesAsList()))

    def isValid(self):

        # Construindo uma string de zeros do tamanho da dificuldade do bloco
        target = "0" * self.difficulty

        # Caso Geral:
        #   Caso o hash do bloco seja diferente do que deveria ser
        #   Ou
        #   Caso o hash do bloco não tenha sido validado pelo PoW
        if(self.currentBlockHash != self.realHash() or
            self.currentBlockHash[:self.difficulty] != target):
            return False

        # Caso específico do bloco genesis:
        if(self.index==1):
            if(self.previousBlockHash != "0"*64):
                return False

        # Caso específico dos outros blocos:
        else:
            previousBlock = Block.objects.get(index=self.index-1)
            # Caso o previousHash do bloco atual seja diferente do hash do bloco anterior
            if(self.previousBlockHash != previousBlock.currentBlockHash):
                return False

        return True

class Vote(AbstractVote):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=False)

    def getBlock(self):
        return (self.block)

class Seeder(AbstractSeeder):
    pass