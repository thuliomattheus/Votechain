import django_tables2 as tables
from clientProject.blockchainReusableApp.models import AbstractSeeder

class SeederTable(tables.Table):
    class Meta:
        model = AbstractSeeder
