from django.db import models
from hashlib import sha256
from nodeProject.nodeApp import utilities

PRESIDENTE = 'PDT'
SENADOR = 'SEN'
GOVERNADOR = 'GOV'
PREFEITO = 'PRF'

ROLES = (
            (PRESIDENTE,'Presidente'),
            (SENADOR, 'Senador'),
            (GOVERNADOR, 'Governador'),
            (PREFEITO, 'Prefeito')
        )

class Block(models.Model):
    index = models.PositiveIntegerField(primary_key=True, blank=False, null=False)
    timestamp = models.DateTimeField(blank=False, null=False)
    votes = models.TextField() # Json com a lista de votos
    difficulty = models.PositiveIntegerField(blank=False, null=False)
    nonce = models.PositiveIntegerField(blank=False, null=False)
    previousBlockHash = models.CharField(max_length=512, blank=False, null=False)
    currentBlockHash = models.CharField(max_length=512, blank=False, null=False)

    def __str__(self):
        return ("Bloco " + str(self.index) + ":\n\n" + self.votes)

    def getAttributesAsList(self):
        return [
                self.index,
                utilities.dateToString(self.timestamp),
                self.votes,
                self.difficulty,
                self.nonce,
                self.previousBlockHash
            ]

class Vote(models.Model):
    voterPubKey = models.CharField(max_length=500, blank=False, null=False)
    candidateRole = models.CharField(choices=ROLES, max_length=30, blank=False, null=False)
    candidateNumber = models.PositiveIntegerField(blank=False, null=False)
    digitalSignature = models.CharField(max_length=100, blank=False, null=False)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return (self.voterPubKey + " votou no(a) candidato(a) à " +
            self.candidateRole + " de número " + str(self.candidateNumber))

    def getCandidatePublicKey(self):
        return (self.candidateRole + str(self.candidateNumber))
