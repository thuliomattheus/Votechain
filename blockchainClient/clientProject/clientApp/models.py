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
        return Vote.userAlreadyVotedOnThisRole(self.id, cargo)

    def getVotedRoles(self):
        return Vote.getVotedRolesByUserId(self.id)

    def getVotes(self):
        return Vote.getVotesByUserId(self.id)

    def getSeeders(self):
        return Seeder.getSeedersByUserId(self.id)

class Vote(AbstractVote):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    @staticmethod
    def userAlreadyVotedOnThisRole(id, role):
        return Vote.getVotedRolesByUserId(id).filter(candidateRole=role).exists()

    @staticmethod
    def getVotedRolesByUserId(id):
        return Vote.getVotesByUserId(id).values('candidateRole').distinct()

    @staticmethod
    def getVotesByUserId(id):
        user = User.objects.get(id=id)
        return Vote.objects.filter(user=user)

class Seeder(AbstractSeeder):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    @staticmethod
    def getSeedersByUserId(id):
        user = User.objects.get(id=id)
        return Seeder.objects.filter(user=user)
