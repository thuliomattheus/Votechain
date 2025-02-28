import django_tables2 as tables
from clientProject.blockchainReusableApp.models import AbstractSeeder, AbstractVote

class SeederTable(tables.Table):
    class Meta:
        model = AbstractSeeder

class VoteTable(tables.Table):
    class Meta:
        model = AbstractVote
        fields = ('candidateRole', 'candidateNumber')
