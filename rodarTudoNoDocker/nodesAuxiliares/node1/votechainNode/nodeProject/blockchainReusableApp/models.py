from django.db import models

class AbstractVote(models.Model):

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

    voterPubKey = models.CharField(max_length=500, blank=False, null=False)
    candidateRole = models.CharField(choices=ROLES, max_length=30, blank=False, null=False, verbose_name='Cargo')
    voterDocument = models.CharField(max_length=12, blank=False, null=False)
    candidateNumber = models.PositiveIntegerField(blank=False, null=False, verbose_name='Número')
    digitalSignature = models.CharField(max_length=350, blank=False, null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return ("Candidato(a) à " + self.candidateRole + " de número " + str(self.candidateNumber))

    def getCandidate(self):
        return (self.candidateRole + str(self.candidateNumber))

class AbstractSeeder(models.Model):
    ip = models.CharField(max_length=15, blank=False, null=False)
    port = models.PositiveIntegerField(blank=False, null=False, verbose_name='Porta')

    class Meta:
        abstract = True

    def __str__(self):
        return("Node rodando em http://" + self.ip + ":" + str(self.port))
