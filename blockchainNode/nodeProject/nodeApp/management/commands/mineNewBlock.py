from django.core.management.base import BaseCommand
from django.utils import timezone
from nodeProject.nodeApp.models import Block, Vote
from nodeProject.nodeApp.serializers import VoteSerializer
from nodeProject.nodeApp.tasks import proofOfWork
from nodeProject.nodeApp import services
from nodeProject.blockchainReusableApp.utilities import verifySignature
import json

class Command(BaseCommand):
    # Informação que será retornada pelo 'python manage.py mineNewBlock'
    help = "Job para criar novos blocos, à partir dos votos"

    def execute(self, *args, **options):

        # Só adiciona novos blocos, se o último já tiver sido validado
        if(services.getBlockchainSyncStatus() == "Válida"):

            # Retorna todos os votos
            allVotes = Vote.objects.all()

            # Remove os votos que não possuem assinatura válida
            for vote in allVotes:
                if(not verifySignature(vote.digitalSignature, vote.getCandidate(), vote.voterPubKey)):
                    print("O voto " + str(vote.id) + " foi removido")
                    Vote.objects.filter(id=vote.id).delete()

            # Votos que serão atribuídos ao novo bloco
            votes = Vote.objects.filter(block_id=None)[0:5]

            # Caso a lista de votos não esteja vazia
            if(votes):

                # Índice do novo bloco
                # Começa com 1
                index = Block.objects.count() + 1

                # Serialização dos votos
                serializedVotes = VoteSerializer(votes, many=True)

                # Conversão dos votos serializados em string
                deserializedVotes = json.dumps(serializedVotes.data, indent=3, ensure_ascii=False)

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
                newBlock = Block(
                    index = index,
                    timestamp = timestamp,
                    votes = deserializedVotes,
                    difficulty = difficulty,
                    nonce = nonce,
                    previousBlockHash = previousBlockHash,
                )

                # Commit no banco
                newBlock.save()
                # Chamada da task assíncrona do "PoW"
                proofOfWork.delay(index)

                # Atribuição do bloco atual aos votos utilizados
                for vote in votes:
                    vote.block = newBlock
                    vote.save()
