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
    pass

class Seeder(AbstractSeeder):
    pass