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

class Vote(AbstractVote):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def getVotesByUser(self, user):
        return Vote.objects.get(user=user)

class Seeder(AbstractSeeder):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def getSeedersByUser(self, user):
        return Seeder.objects.get(user=user)
