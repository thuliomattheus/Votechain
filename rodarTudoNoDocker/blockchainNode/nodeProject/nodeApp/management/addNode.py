"""
from django.core.management.base import BaseCommand
from nodeProject.nodeApp.models import Seeder
from nodeProject.nodeApp.serializers import SeederSerializer
from nodeProject.nodeApp.forms import SeederForm

class Command(BaseCommand):
    # Informação que será retornada pelo 'python manage.py addNode -h'
    help = "Job para adicionar um novo node, aos nodes conhecidos"

    def execute(self, *args, **options):

        ip = 3
        port = port
        host = host

        node = new SeederForm()

        if(node.is_valid()):
            node.save()

        # Criação de um novo objeto do tipo Seeder,
        # passando o ip e/ou o host, assim como a porta
        newNode = Seeder(
            ip = ip,
            port = port,
            host = host,
        )

        # Commit no banco
        newNode.save()

"""