from __future__ import absolute_import
from nodeProject.nodeApp import services
from nodeProject.nodeApp.models import Seeder, Block, Vote
from nodeProject.nodeApp.serializers import VoteSerializer
from nodeProject.nodeApp.utilities import concatenate, encryptSha256, dateToString
from nodeProject.blockchainReusableApp.utilities import verifySignature
from django.utils import timezone
from celery import shared_task
from celery import task
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Broadcast dos votos
@shared_task
def broadcastVote(vote, myIp, myPort):

    # Broadcast do voto para os nodes conhecidos
    for node in Seeder.objects.all():

        # Link das apis rest dos nodes conhecidos
        url = 'http://'+ node.ip + ':' + str(node.port) + '/blockchain/vote/'

        # Garantindo que um node não envie voto para ele mesmo
        #
        # Para isso, ou a primeira parte do ip é diferente,
        # Ou a porta é diferente
        if(node.ip.split('.')[0] != myIp.split('.')[0] or node.port != myPort):
            try:
                # Envio de uma requisição que envia o voto para a url definida
                jsonResponse = requests.post(url, data=vote, timeout=5)
                logger.debug("Pra essa url: " + url + " funcionou")
            # Caso algum erro de conexão aconteça
            except:
                logger.debug("Pra essa url: " + url + " não funcionou")

# Mineração do bloco
@shared_task
def proofOfWork(blockId):

    # Busca pelo objeto
    block = Block.objects.get(index=blockId)

    # Construindo uma string de zeros do tamanho da dificuldade da blockchain
    difficulty = block.difficulty
    target = "0" * difficulty

    # Cópia do hash e do nonce do bloco atual
    # para serem realizados cálculos em memória,
    # impedindo a perda de desempenho que haveria
    # ao ficar atualizando os dados diretamente no banco
    currentHash = block.currentBlockHash
    currentNonce = 0

    # Enquanto os 'n = difficulty' primeiros caracteres
    # do hash atual não forem iguais a zero,
    # incrementar o nonce e recalcular o hash
    while(currentHash[:difficulty] != target):
        # Atualização dos dados em memória
        currentNonce = currentNonce + 1
        currentTimestamp = timezone.now()
        currentHash = encryptSha256(
                concatenate(
                    [
                        block.index,
                        dateToString(currentTimestamp),
                        block.votes,
                        block.difficulty,
                        currentNonce,
                        block.previousBlockHash
                    ]
                )
            )
    block.nonce = currentNonce
    block.timestamp = currentTimestamp
    block.currentBlockHash = currentHash
    block.save()

@shared_task(name="mine_new_block")
def mineNewBlock():

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
