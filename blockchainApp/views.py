from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .models import *
import json
from rest_framework import viewsets
from . import blockchain
from .serializers import BlockSerializer

class BlockViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = BlockSerializer

    def list(self, request):
        serializer = BlockSerializer(
            instance = blockchain.main(),
            many=True)
        return HttpResponse(json.dumps(serializer.data, indent=3), content_type='json')

def listarUsuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listarUsuarios.html', {'users' : usuarios})

def detalharUsuario(request, idUsuario):
    usuario = get_object_or_404(Usuario, pk=idUsuario)
    dados = {'user' : usuario}
    return render(request, 'verAmigos.html', dados)

"""
def minerarBloco(request, blocoId):
    block = get_object_or_404(Block, pk=blocoId)
    block.setHash()
    block.save()
    dados = {'bloco' : block, 'blocoId' : blocoId}
    return render(request, 'verDados.html', dados)
"""
