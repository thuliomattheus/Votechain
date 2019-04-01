from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from nodeProject.nodeApp.serializers import *
from nodeProject.nodeApp.models import Block, Vote
from nodeProject.nodeApp.services import proofOfWork, getCurrentDifficulty, isChainValid
import json

class Vote(CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

class BlockDetail(RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    """
    # Acesso através do método POST do HTTP
    def create(self, request, format=None):
        # Serializar os dados da requisição
        serializer = self.get_serializer(data=request.data)
        # Validação dos dados serializados
        serializer.is_valid(raise_exception=True)
        # Gravação dos dados no arquivo da blockchain
        serializer.save()
        # Pegando o cabeçalho de sucesso
        headers = self.get_success_headers(serializer.data)
        # Renderizando os dados serializados
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Acesso através do método GET do HTTP
    def list(self, request, *args, **kwargs):
        # Executa o queryset e aplica os filtros passados, se houverem
        instance = self.filter_queryset(self.get_queryset())
        # Guarda os argumentos de paginação, se houverem
        page = self.paginate_queryset(instance)
        # Verifica a necessidade de paginação
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = BlockSerializer(instance, many=True)
        # Renderização da página
        return Response(serializer.data)
        """

# Recuperar a lista de blocos
@api_view(['GET'])
def BlockList(request):

    queryset = []

    for block in Block.objects.all():
        if(block.isValid()):
            queryset.append(block)

    return Response(
        BlockchainSerializer(
            instance = queryset,
            many = True,
            context = {
                'request':request
            }
        ).data)


# Recuperar as informações básicas da cadeia
@api_view(['GET'])
def Status(request):
    queryset = [{
        "depth" : Block.objects.count(),
        "difficulty" : getCurrentDifficulty(),
        "status" : isChainValid()
    }]
    return Response(InfoChainSerializer(queryset, many=True).data)

# Recuperar o último bloco
@api_view(['GET'])
def LastBlock(request):
    if(Block.objects.count()==0):
        return Response([])
    else:
        queryset = [Block.objects.order_by('-pk')[0]]
        return Response(BlockSerializer(queryset, many=True).data)

"""
    with open("nodeProject/nodeApp/blockchain2.json", "a") as write_file:
        json.dump(serializer.data, write_file)

    with open("nodeProject/nodeApp/blockchain.json", "r") as read_file:
        blockchainData = json.load(read_file)
    return JsonResponse(blockchainData, json_dumps_params={'indent':3, 'ensure_ascii':False}, safe=False)
"""