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

            # Lista de votos extras que um usuário possui
            extraVotes = []

            for vote in Vote.objects.all():
                message = vote.getCandidate() + ":" + vote.voterDocument
                # Remove os votos que não possuem assinatura válida
                if(not verifySignature(vote.digitalSignature, message , vote.voterPubKey)):
                    print("O voto " + str(vote.id) + " foi removido")
                    Vote.objects.filter(id=vote.id).delete()
                # Busca por votos que possuem o mesmo cargo e o mesmo título
                if(len(Vote.getVotesOnRoleByVoterDocument(vote.voterDocument, vote.candidateRole))>1):
                    # Caso o voto ainda não esteja na lista, adicione-o
                    if(extraVotes.count([vote.voterDocument, vote.candidateRole])==0):
                        extraVotes.append([vote.voterDocument, vote.candidateRole])

            # Remove os votos extras que algum usuário possa ter feito em um dado cargo
            for voterDocument, candidateRole in extraVotes:
                # Busca todos os votos extras do mesmo usuario no mesmo cargo
                votes = Vote.getVotesOnRoleByVoterDocument(voterDocument, candidateRole)
                # Percorre-os
                for vote in votes :
                    # Caso ele não seja o primeiro, apague-o
                    if(vote.id is not Vote.getFirstVoteOnRoleByVoterDocument(voterDocument, candidateRole)):
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
