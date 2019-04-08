from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from nodeProject.nodeApp.serializers import *
from nodeProject.nodeApp.models import Block, Vote
from nodeProject.nodeApp import services
from django.http import JsonResponse

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
    return Response(BlockchainStatusSerializer(queryset).data)

# Recuperar o último bloco válido
@api_view(['GET'])
def LastValidBlock(request):
    lastValidBlockIndex = services.getLastValidBlockIndex()
    return Response(LastBlockSerializer(lastValidBlockIndex).data)

class Vote(CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

def miningBlock(request):
    while(services.getBlockchainStatus().get('status')=="Validando"):
        continue
    return JsonResponse({ 'status' : 'OK'})