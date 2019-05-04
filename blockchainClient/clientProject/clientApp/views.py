from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from clientProject.clientApp.models import Vote, User
from clientProject.clientApp.forms import RegisterForm, VoteForm
from clientProject.blockchainReusableApp.utilities import generateKeys, signMessage, verifySignature
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

            url = 'http://localhost:8000/blockchain/vote/'
            jsonResponse = requests.post(url, data=vote.__dict__)

            return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
    else:
        form = VoteForm()
    return render(request, 'vote.html', {'form': form})
