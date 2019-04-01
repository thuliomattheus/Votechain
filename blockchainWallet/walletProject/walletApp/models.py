from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=80, blank=False, null=False)
    rg = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11, blank=False, null=False)
    tituloEleitor = models.CharField(max_length=12, blank=False, null=False)
    email = models.CharField(max_length=64, blank=False, null=False)
    username = models.CharField(max_length=64, blank=False, null=False)
    password = models.CharField(max_length=64, blank=False, null=False)
    publicKey = models.CharField(max_length=5, blank=False, null=False)
    privateKey = models.CharField(max_length=5, blank=False, null=False)

    def __str__(self):
        return (self.nome)

class Vote(models.Model):
    voterPubKey = models.CharField(max_length=500, blank=False, null=False)
    candidateRole = models.CharField(choices=ROLES, max_length=30, blank=False, null=False)
    candidateNumber = models.PositiveIntegerField(blank=False, null=False)
    digitalSignature = models.CharField(max_length=100, blank=False, null=False)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=False)
