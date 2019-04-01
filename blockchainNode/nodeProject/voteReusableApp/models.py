from django.db import models

PRESIDENTE = 'Presidente'
SENADOR = 'Senador'
GOVERNADOR = 'Governador'
PREFEITO = 'Prefeito'

ROLES = (
            (PRESIDENTE,'Presidente'),
            (SENADOR, 'Senador'),
            (GOVERNADOR, 'Governador'),
            (PREFEITO, 'Prefeito')
        )

class AbstractVote(models.Model):

    voterPubKey = models.CharField(max_length=500, blank=False, null=False)
    candidateRole = models.CharField(choices=ROLES, max_length=30, blank=False, null=False)
    candidateNumber = models.PositiveIntegerField(blank=False, null=False)
    digitalSignature = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return (self.voterPubKey + " votou no(a) candidato(a) à " +
            self.candidateRole + " de número " + str(self.candidateNumber))

    def getCandidatePublicKey(self):
        return (self.candidateRole + str(self.candidateNumber))
