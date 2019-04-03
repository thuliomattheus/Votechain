from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from nodeProject.nodeApp.serializers import *
from nodeProject.nodeApp.models import Block, Vote
from nodeProject.nodeApp import services

# Recupera os dados do bloco
@api_view(['GET'])
def BlockDetail(request, pk):

    block = get_object_or_404(Block, index=pk)

    return Response(BlockSerializer(block).data)

# Recupera a lista de blocos
@api_view(['GET'])
def BlockList(request):

    blocks = Block.objects.all()
    return Response(BlockchainSerializer(blocks, many=True, context = {'request':request}).data)

# Recuperar as informações básicas da cadeia
@api_view(['GET'])
def Status(request):
    queryset = services.getBlockchainStatus()
    return Response(BlockchainStatusSerializer(queryset, many=True).data)

# Recuperar o último bloco válido
@api_view(['GET'])
def LastValidBlock(request):

    lastValidBlockIndex = services.getLastValidBlockIndex()

    # Se nenhum bloco for válido, retorne uma mensagem indicativa
    if(lastValidBlockIndex==None):
        return Response(" A blockchain não possui blocos válidos! ")

    # Se a blockchain estiver vazia, retorne uma lista vazia
    elif(lastValidBlockIndex==0):
        return Response([])

    else:
        block = Block.objects.get(index=lastValidBlockIndex)
        return Response(BlockSerializer([block], many=True).data)

class Vote(CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer