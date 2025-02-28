from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from nodeProject.nodeApp.serializers import *
from nodeProject.nodeApp.models import Block, Vote, Seeder
from nodeProject.nodeApp.tasks import broadcastVote
from nodeProject.nodeApp.utilities import getIpAndPort, isAddressValid
from nodeProject.nodeApp import services
from django.http import JsonResponse
from nodeProject.blockchainReusableApp.utilities import verifySignature
from nodeProject.blockchainReusableApp.tables import SeederTable
from django_tables2 import RequestConfig
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Recupera a lista de blocos
@api_view(['GET'])
def BlockList(request):
    blocks = Block.objects.all()
    return Response(BlockchainSerializer(blocks, many=True, context = {'request':request}).data)

# Recupera os dados do bloco
@api_view(['GET'])
def BlockDetail(request, pk):
    block = get_object_or_404(Block, index=pk)
    return Response(BlockSerializer(block).data)

# Recuperar os dados do último bloco válido
@api_view(['GET'])
def LastValidBlock(request):
    lastValidBlockIndex = services.getLastValidBlockIndex()
    return Response(LastBlockSerializer(lastValidBlockIndex).data)

# Recuperar as informações básicas da cadeia
@api_view(['GET'])
def Status(request):
    ip, port = getIpAndPort(request)
    queryset = services.getBlockchainStatus(ip, port)
    return Response(BlockchainStatusSerializer(queryset).data)

# Realizar o voto
@api_view(['POST'])
def ToVote(request):
    form = VoteSerializer(data=request.data)
    if(form.is_valid()):
        vote = form.validated_data

        # Verificação se alguém com esse título, já votou nesse cargo
        if(Vote.userAlreadyVotedOnThisRole(vote['voterDocument'], vote['candidateRole'])):
            logger.info('Voto inválido! Eleitor já votou nesse cargo!')
            return JsonResponse({ 'status' : 'Voto inválido! Eleitor já votou nesse cargo!'})

        # Formatação da mensagem que representará o voto
        message = vote['candidateRole'] + str(vote['candidateNumber']) + ":" + vote['voterDocument']

        # Caso a assinatura digital seja válida
        if(verifySignature(vote['digitalSignature'], message, vote['voterPubKey'])):

            # Endereço local próprio
            myIp, myPort = getIpAndPort(request)

            # Salva o voto no banco
            form.save()

            # Envia o voto para os nodes conhecidos
            broadcastVote.delay(vote, myIp, myPort)

            return JsonResponse({ 'status' : 'Voto cadastrado com sucesso!'})
    return JsonResponse({ 'status' : 'Voto inválido!'})

# Iniciar uma conexão com outro node
@api_view(['POST'])
def ToConnect(request):

    form = SeederSerializer(data=request.data)

    if(form.is_valid()):
        # Guarda os dados do form para manipulação
        newNode = form.validated_data

        # Endereço do node
        newNodeAddress = newNode['ip'] + ':' + str(newNode['port'])

        # Verifica se o endereço é válido
        if(isAddressValid(newNodeAddress)):

            # Url do status do node
            url = 'http://' + newNodeAddress + '/blockchain/status/'

            # Endereço local próprio
            myIp, myPort = getIpAndPort(request)

            # Garantindo que um node não crie solicitação para ele mesmo
            #
            # Para isso, ou a primeira parte do ip é diferente,
            # Ou a porta é diferente
            if(newNode['ip'].split('.')[0] != myIp.split('.')[0] or str(newNode['port']) != myPort):
                try:
                    # Verifica se o node solicitante é válido
                    jsonResponse = requests.get(url)
                    content = jsonResponse.json()
                    if(content['SyncStatus']=="Válida"):
                        form.save()
                        return JsonResponse({ 'status' : 'Node válido!'})
                # Caso algum erro de conexão aconteça
                except requests.exceptions.ConnectionError as e:
                    return JsonResponse({ 'status' : 'Conexão não pôde ser realizada!'})
                except Exception as e:
                    print(type(e))
            # Caso algum erro de conexão aconteça
            else:
                return JsonResponse({ 'status' : 'Tentativa de autoconexão!'})
    return JsonResponse({ 'status' : 'Node inválido!'})

# Sincronizar a lista de blocos
@api_view(['GET'])
def SynchronizeAllBlocks(request):
    blockchain = Block.objects.all()
    return Response(FullBlockchainSerializer(blockchain, many=True, context = {'request':request}).data)

@api_view(['GET'])
def ConnectedNodes(request):
    queryset = Seeder.objects.all()
    return Response(SeederSerializer(queryset, many=True).data)