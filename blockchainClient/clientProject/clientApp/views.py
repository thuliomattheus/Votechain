from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from clientProject.clientApp.models import Vote, User
from clientProject.clientApp.forms import RegisterForm, VoteForm
from clientProject.clientApp.utilities import generateKeys, signMessage, verifySignature
from django.contrib.auth.decorators import login_required

def register(request):
    if(request.method=='POST'):
        form = RegisterForm(request.POST)
        if(form.is_valid()):
            user = form.save(commit=False)
            user.privateKey, user.publicKey = generateKeys()
            user.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def vote(request):
    if(request.method=='POST'):
        form = VoteForm(request.POST)
        if(form.is_valid()):
            vote = form.save(commit=False)
            vote.voterPubKey = request.user.publicKey
            vote.digitalSignature = signMessage(
                request.user.privateKey,
                str(form.fields['candidateRole'])+str(form.fields['candidateNumber'])
            )
            vote.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
    else:
        form = VoteForm()
    return render(request, 'vote.html', {'form': form})

@login_required
def teste2(request):
    message = "oi muchachos"
    verification = verifySignature(signature, message, request.user.publicKey)
    teste = "\nMensagem verificada" if verification else "\nDEU ERRADO"
    verification = verifySignature(signature, message+"\n", request.user.publicKey)
    teste += "\nMensagem verificada" if verification else "\nDEU ERRADO"
    verification = verifySignature(signature, message, request.user.publicKey)
    teste += "\nMensagem verificada" if verification else "\nDEU ERRADO"

    return render(request, 'teste.html', {'teste': teste})

@login_required
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
