from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import requests
from clientProject.clientApp.serializers import VoterSerializer
from clientProject.clientApp.models import Vote, User
from clientProject.clientApp.forms import LoginForm, RegisterForm
from clientProject.clientApp.utilities import generateKeys

def login(request):
    form = LoginForm()
    if(request.method=='POST'):
        print("5555555555555555555")
    return render(request, 'login.html', {'form': form})

def register(request):
    form = RegisterForm()
    if(request.method=='POST'):
        print(generateKeys()[1])
    return render(request, 'register.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def teste(request):
    url = 'http://localhost:8000/blockchain/vote/'
    data = {
        'voterPubKey': 123,
        'candidateRole': Vote.SENADOR,
        'candidateNumber': 123,
        'digitalSignature': '7897z9asas979sasdasd'
    }
    jsonResponse = requests.post(url, data=data)

    return HttpResponse(jsonResponse, content_type="application/json")
