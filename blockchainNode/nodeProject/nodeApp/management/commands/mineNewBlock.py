from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from nodeProject.nodeApp.models import Block, Vote
from nodeProject.nodeApp.serializers import VoteSerializer
from nodeProject.nodeApp import services
from nodeProject.nodeApp import utilities
import os
import json

class Command(BaseCommand):
    # Informação que será retornada pelo 'python manage.py mineNewBlock'
    help = "Job para criar novos blocos, à partir dos votos"

    def execute(self, *args, **options):

        # Só adiciona novos blocos, se o último já tiver sido validado
        if(services.getBlockchainSyncStatus() == "Válida"):

            # Votos que serão atribuídos ao novo bloco
            queryset = Vote.objects.filter(block_id=None)[0:5]

            # Caso a lista de votos não esteja vazia
            if(queryset):

                # Índice do novo bloco
                # Começa com 1
                index = Block.objects.count() + 1

                # Serialização dos votos
                serializer = VoteSerializer(queryset, many=True)

                # Conversão dos votos serializados em string
                votes = json.dumps(serializer.data, indent=3, ensure_ascii=False)

                # Caso o bloco adicionado seja o bloco genesis
                if(index == 1):
                    previousBlockHash = "0" * 64
                # Caso contrário
                else:
                    # Recupere o hash atual do último bloco da blockchain
                    previousBlockHash = Block.objects.order_by('-pk')[0].currentBlockHash

                # Incrementador inicial utilizado na mineração do bloco
                nonce = 0

                # Dificuldade do bloco
                difficulty = services.getCurrentDifficulty()

                # Data e hora da criação do bloco
                timestamp = timezone.now()

                # Criação de um novo objeto do tipo Bloco,
                # passando apenas os votos e o hash anterior
                novoBloco = Block(
                    index = index,
                    timestamp = timestamp,
                    votes = votes,
                    difficulty = difficulty,
                    nonce = nonce,
                    previousBlockHash = previousBlockHash,
                )

                # Commit no banco
                novoBloco.save()

                # Atribuição do bloco atual aos votos utilizados
                for voto in queryset:
                    voto.block = novoBloco
                    voto.save()