from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_tables2 import RequestConfig
from clientProject.clientApp.models import Vote, User, Seeder
from clientProject.clientApp.forms import RegisterForm, VoteForm, SeederForm
from clientProject.clientApp.utilities import encryptSha256, writeMessageOnFile
from clientProject.blockchainReusableApp.tables import SeederTable
from clientProject.blockchainReusableApp.utilities import generateKeys, signMessage, verifySignature
import requests

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
            writeMessageOnFile(originalPrivateKey, 'privateKey'+user.username.title())

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

            # Associação do voto, ao atual usuário
            vote.user = request.user

            # Flag para saber se ao menos um node, recebeu o voto
            voteFlag = False
            # Mensagem que será exibida na tela do cliente
            message = ''

            # Requisição do voto à todos os nodes conhecidos
            for node in request.user.getSeeders():

                # Link das apis rest dos nodes conhecidos
                url = 'http://'+ node.ip + ':' + str(node.port) + '/blockchain/vote/'

                try:
                    # Envio de uma requisição que envia o voto para a url definida
                    jsonResponse = requests.post(url, data=vote.__dict__)
                    # Caso nenhum node tenha recebido votos ainda
                    if(not voteFlag):
                        voteFlag = True
                        message = jsonResponse.json()['status']
                except requests.exceptions.ConnectionError as e:
                    if(not voteFlag):
                        message = 'Não foi possível conectar com nenhum node!'

            # Verifica se o voto foi enviado à ao menos um node
            if(voteFlag):
                messages.success(request, message)
                vote.save()
            else:
                # Mensagem de falha
                messages.error(request, message)

            # Redirecionamento do usuário para sua tela principal
            return HttpResponseRedirect(reverse('login'))

        else:
            print(form.errors)
    else:
        form = VoteForm()
    return render(request, 'vote.html', {'form': form})

@login_required
def addSeeder(request):

    # Caso a requisição seja 'POST'
    if(request.method=='POST'):

        # Inicialização do formulário
        form = SeederForm(request.POST)

        # Verificação dos dados do formulário
        if(form.is_valid()):

            # Salva os dados em uma variável auxiliar para poder manuseá-los
            seeder = form.save(commit=False)

            # Associação do node, ao atual usuário
            seeder.user = request.user

            # Salva os dados no banco
            seeder.save()

            messages.success(request, 'Novo node adicionado!')

            # Redirecionamento do usuário para sua tela principal
            return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
    else:
        form = SeederForm()
    return render(request, 'addSeeder.html', {'form': form})

def showSeederList(request):
    if(request.method=='GET'):
        table = SeederTable(request.user.getSeeders(), order_by=('ip', 'port'))
        RequestConfig(request, paginate={'per_page': 5}).configure(table)

    return render(request, 'seederList.html', {'table': table})