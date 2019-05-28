from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from nodeProject.nodeApp.serializers import *
from nodeProject.nodeApp.models import Block, Vote, Seeder
from nodeProject.nodeApp.tasks import broadcastVote
from nodeProject.nodeApp import services
from django.http import JsonResponse
from nodeProject.blockchainReusableApp.utilities import verifySignature
from nodeProject.blockchainReusableApp.tables import SeederTable
from django_tables2 import RequestConfig
import requests

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
    queryset = services.getBlockchainStatus()
    return Response(BlockchainStatusSerializer(queryset).data)

# Realizar o voto
@api_view(['POST'])
def ToVote(request):
    form = VoteSerializer(data=request.data)
    if(form.is_valid()):
        vote = form.validated_data
        candidate = vote['candidateRole'] + str(vote['candidateNumber'])
        if(verifySignature(vote['digitalSignature'], candidate, vote['voterPubKey'])):
            form.save()
            broadcastVote.delay(vote)
            return JsonResponse({ 'status' : 'Voto cadastrado com sucesso!'})
    return JsonResponse({ 'status' : 'Voto inválido!'})

# Iniciar uma conexão com outro node
@api_view(['POST'])
def ToConnect(request):
    form = SeederSerializer(data=request.data)

    if(form.is_valid()):
        newNode = form.validated_data

        # Link do novo node
        url = 'http://'+ newNode['ip'] + ':' + str(newNode['port']) + '/blockchain/status/'

        try:
            jsonResponse = requests.get(url)
            content = jsonResponse.json()
            if(content['Current Sync Status']=="Válida"):
                newNode.save()
                return JsonResponse({ 'status' : 'Node válido!'})
        except requests.exceptions.ConnectionError as e:
            return JsonResponse({ 'status' : 'Conexão não pôde ser realizada!'})

    return JsonResponse({ 'status' : 'Node inválido!'})

# Sincronizar a lista de blocos
@api_view(['GET'])
def SynchronizeBlocks(request):
    blockchain = Block.objects.all()
    return Response(FullBlockchainSerializer(blockchain, many=True, context = {'request':request}).data)

# Sincronizar a lista de nodes
@api_view(['GET'])
def SynchronizeNodes(request):
    seederList = Seeder.objects.all()
    return Response(SeederSerializer(seederList, many=True, context = {'request':request}).data)
