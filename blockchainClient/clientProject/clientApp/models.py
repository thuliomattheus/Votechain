from django.db import models
from clientProject.blockchainReusableApp.models import AbstractVote, AbstractSeeder
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    cpf = models.CharField(max_length=11, blank=False, null=False)
    voterDocument = models.CharField(max_length=12, blank=False, null=False)
    publicKey = models.CharField(max_length=64, blank=False, null=False)
    privateKey = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return (self.username)

    def alreadyVotedOnThisRole(self, cargo):
        return Vote.userAlreadyVotedOnThisRole(self.voterDocument, cargo)

    def getVotedRoles(self):
        return Vote.getVotedRolesByVoterDocument(self.voterDocument)

    def getVotes(self):
        return Vote.getVotesByVoterDocument(self.voterDocument)

    def getSeeders(self):
        return Seeder.getSeedersByUserId(self.id)

class Vote(AbstractVote):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    @staticmethod
    def userAlreadyVotedOnThisRole(voterDocument, role):
        return Vote.getVotedRolesByVoterDocument(voterDocument).filter(candidateRole=role).exists()

    @staticmethod
    def getVotedRolesByVoterDocument(voterDocument):
        return Vote.getVotesByVoterDocument(voterDocument).values('candidateRole').distinct()

    @staticmethod
    def getVotesByVoterDocument(voterDocument):
        return Vote.objects.filter(voterDocument=voterDocument)

class Seeder(AbstractSeeder):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    @staticmethod
    def getSeedersByUserId(id):
        user = User.objects.get(id=id)
        return Seeder.objects.filter(user=user)
