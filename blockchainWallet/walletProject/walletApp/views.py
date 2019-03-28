from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
import requests

def listarUsuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listarUsuarios.html', {'users' : usuarios})

def detalharUsuario(request, idUsuario):
    usuario = get_object_or_404(Usuario, pk=idUsuario)
    dados = {'user' : usuario}
    return render(request, 'verAmigos.html', dados)

def teste(request):
    url = 'http://localhost:8000/router/blocks/' 
    #params = {'year': year, 'author': author}
    #r = requests.get(url, params=params)
    jsonResponse = requests.get(url)

    return HttpResponse(jsonResponse, content_type="application/json")
