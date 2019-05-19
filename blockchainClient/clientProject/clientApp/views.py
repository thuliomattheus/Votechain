from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from clientProject.clientApp.models import Vote, User
from clientProject.clientApp.forms import RegisterForm, VoteForm
from clientProject.blockchainReusableApp.utilities import generateKeys, signMessage, verifySignature
from django.contrib.auth.decorators import login_required
from clientProject.clientApp.utilities import encryptSha256, writeMessageOnFile
from django.contrib import messages

# Registrar novo usuário na aplicação cliente
def register(request):
    # Caso a requisição seja 'POST'
    if(request.method=='POST'):

        # Inicialização do formulário
        form = RegisterForm(request.POST)

        # Verificação dos dados do formulário
        if(form.is_valid()):

            # Criação de uma instância de usuário com os dados do formulário
               # Entretanto, nenhum dado foi salvo no dados no banco
            user = form.save(commit=False)

            # Criação das chaves privada e pública,
                # Atribuição da chave pública em seu formato real, ao usuário;
                # Criação de uma variável auxiliar para manipulação da chave privada
            originalPrivateKey, user.publicKey = generateKeys()

            # Criação de um arquivo para guardar a chave privada real, localmente
            writeMessageOnFile(originalPrivateKey)

            # Atribuição da chave privada criptografada ao usuário
                # Com isso, a mesma pode ser guardada com segurança no banco
            user.privateKey = encryptSha256(originalPrivateKey)

            # Persistência dos dados no banco
            user.save()

            messages.success(request, 'Sua conta foi criada com sucesso!')

            # Redirecionamento para a tela de login
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

    # Caso a requisição seja 'POST'
    if(request.method=='POST'):

        # Inicialização do formulário
        form = VoteForm(request.POST, request.FILES)

        # Verificação dos dados do formulário
        if(form.is_valid()):

            # Criação de uma instância de voto com os dados do formulário
               # Entretanto, nenhum dado foi salvo no dados no banco
            vote = form.save(commit=False)

            # Atribuição do conteúdo do arquivo, à uma variável auxiliar para manuseio
            fileContent = form.cleaned_data['privateKey'].read().decode('utf-8')

            # Verifica se o conteúdo do arquivo corresponde a sua própria chave privada
            if(encryptSha256(fileContent) != request.user.privateKey):

                # Mensagem informando que a chave privada não corresponde ao usuário
                messages.error(request, 'Chave privada incorreta!')

                return render(request, 'vote.html', {'form': form})

            # Atribuição da chave pública com os dados do usuário logado
            vote.voterPubKey = request.user.publicKey

            # Criação da assinatura digital
                # Parâmetros:
                    # O conteúdo do arquivo que guarda a chave privada do usuário;
                    # O voto do usuário no formato: (função + número)
            vote.digitalSignature = signMessage(
                fileContent,
                vote.getCandidate()
            )

            # Persistência dos dados no banco de dados
            vote.save()

            messages.success(request, 'Seu voto foi enviado com sucesso!')

            # Link da api rest do node
            url = 'http://localhost:8000/blockchain/vote/'

            # Envio de uma requisição que envia o voto para a url definida
            jsonResponse = requests.post(url, data=vote.__dict__)

            # Resposta da requisição
            print(jsonResponse.json()['status'])

            # Redirecionamento do usuário para sua tela principal
            return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
    else:
        form = VoteForm()
    return render(request, 'vote.html', {'form': form})
