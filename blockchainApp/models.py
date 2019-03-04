from django.db import models
from django.utils import timezone
from hashlib import sha256

class Usuario(models.Model):

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    rg = models.CharField(max_length=15, blank=True)
    cpf = models.CharField(max_length=11, blank=True)
    tituloEleitor = models.CharField(max_length=12, blank=True)
    email = models.CharField(max_length=64, blank=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=False)
    publicKey = models.CharField(max_length=5, blank=True)
    privateKey = models.CharField(max_length=5, blank=True)
    amigos = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return (self.nome)

""" 

    def getAttributesAsString(self):
        return (self.data + " " + str(self.index) + " " + 
                self.timestamp.strftime("%d/%m/%y - %T") +
                " " + self.previousHash + " " + str(self.nonce))

    def showFullData(self):
        return (" Índice        : " + str(self.index) + "\n" +
               " Timestamp     : " + self.timestamp.strftime("%d/%m/%y - %T") + "\n" +
               " Dados         : " + self.data + "\n" +
               " Nonce         : " + str(self.nonce) + "\n" +
               " Hash Anterior : " + self.previousHash + "\n" +
               " Hash Atual    : " + self.hash+"\n")

    def setHash(self):
       self.hash = sha256(self.getAttributesAsString().encode()).hexdigest()
 """