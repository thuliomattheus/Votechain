from __future__ import absolute_import
from nodeProject.nodeApp.models import Seeder, Block
from nodeProject.nodeApp.utilities import concatenate, encryptSha256, dateToString
from celery import shared_task
import requests
from django.utils import timezone

# Broadcast dos votos
@shared_task
def broadcastVote(vote):

    # Broadcast do voto para os nodes conhecidos
    for node in Seeder.objects.all():

        # Link das apis rest dos nodes conhecidos
        url = 'http://'+ node.ip + ':' + str(node.port) + '/blockchain/vote/'

        try:
            # Envio de uma requisição que envia o voto para a url definida
            jsonResponse = requests.post(url, data=vote, timeout=5)
            print("Pra essa url: " + url + " funcionou")
        except requests.exceptions.ConnectionError as e:
            print("Pra essa url: " + url + " deu ruim")
            pass

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
