from nodeProject.nodeApp.models import Block, Seeder
from django.dispatch import receiver
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verificação da validação da blockchain
def getBlockchainSyncStatus():

    blockchain = Block.objects.all()

    # Se não houverem blocos, é válida
    if(not blockchain):
        return "Válida"

    # Percorra os blocos da blockchain
    for currentBlock in blockchain:
        # Se algum bloco não for válido
        if(not currentBlock.isValid()):
            # Verificar se é o último e se ele está no proofOfWork
            if(currentBlock.index == len(blockchain) and
                currentBlock.currentBlockHash=="1"*64):
                return "Validando"
            # Caso contrário, a blockchain inteira está inválida
            return "Inválida"
    # Se todos os blocos forem válidos
    return "Válida"

# Função para retornar a dificuldade atualizada do bloco atual
def getCurrentDifficulty():

    # Quantidade de blocos por "rodada"
    # A cada n="roundSize" blocos, atualizar a dificuldade
    roundSize = 5

    # Tamanho atual da blockchain
    blockchainLength = Block.objects.count()

    # Dificuldade inicial da blockchain
    if(blockchainLength==0):
        return 4

    else:

        # Último bloco
        lastBlock = Block.objects.get(index = blockchainLength)
        # Dificuldade do último bloco
        lastBlockDifficulty = lastBlock.difficulty

        # Atualizar a dificuldade entre cada rodada
        if(blockchainLength%roundSize==0):

            # Índice da rodada anterior
            lastRoundIndex = (blockchainLength//roundSize)
            # Primeiro bloco da rodada anterior
            lastRoundFirstBlock = Block.objects.get(index = roundSize * (lastRoundIndex-1) + 1)
            # Período de minutos entre o primeiro e o último bloco da última rodada
            minuteDifference = (lastBlock.timestamp - lastRoundFirstBlock.timestamp).seconds/60

            # Caso demore menos de 3 minutos por bloco
            if(minuteDifference < (3 * roundSize)):
                return lastBlockDifficulty + 1

            # Caso demore mais de 5 minutos por bloco
            elif(minuteDifference > (5 * roundSize)):
                return lastBlockDifficulty - 1

        # Repete a dificuldade do bloco anterior
        return lastBlockDifficulty

# Função para retornar o último bloco da blockchain ou None
def getLastValidBlockIndex():

    # Se a blockchain estiver vazia, retorne 0
    if(Block.objects.count()==0):
        return 0

    else:
        # Caso a blockchain seja válida ou esteja em validação
        if(getBlockchainSyncStatus()!="Inválida"):
            # Percorra-a de maneira decrescente
            for block in Block.objects.order_by('-pk'):
                # Retorne o primeiro bloco válido encontrado
                if(block.isValid()):
                    return block.index

        # Caso a blockchain seja inválida
        else:
            # Percorra-a de maneira crescente
            for block in Block.objects.order_by('pk'):
                # Itere até encontrar um bloco inválido
                if(not block.isValid()):
                    # Caso o primeiro bloco inválido, seja o primeiro bloco da cadeia
                    if(block.index==1):
                        return -1
                    # Retorne o bloco anterior
                    else:
                        return (block.index-1)

        # Se nenhum bloco for válido, retorne -1
        return -1

# Função para saber se o bloco é válido, quando a cadeia é inválida
def isBlockValid(block):
    return True if block.index <= getLastValidBlockIndex() else False

# Função para mostrar as principais informações da blockchain
def getBlockchainStatus(ip, port):
    return {
        'size' : Block.objects.count(),
        'difficulty' : getCurrentDifficulty(),
        'status' : getBlockchainSyncStatus(),
        'connectedNodes' : Seeder.objects.count(),
        'ip': ip,
        'port': port
    }

# Função para descobrir qual a blockchain mais longa da rede
def getLongestBlockchain():
    # Quantidade de blocos do próprio node
    myLength = Block.objects.count()
    # Id do node que possui a maior quantidade de blocos
    node = 0
    # Quantidade de blocos do node com mais blocos
    maxLength = myLength

    # Para todos os nodes conhecidos, acesse seu status
    for seeder in Seeder.objects.all():
        url = 'http://' + seeder.ip + ":" + str(seeder.port) + '/blockchain/status/'

        try:
            # Envia uma requisição para a página de status do node conhecido
            response = requests.get(url)
            # Guarda a quantidade de blocos do node
            nodeLength = response.json()['Blocks']
            # Guarda o status do node
            nodeStatus = response.json()['SyncStatus']
            # Caso o node possua mais blocos do que todos já verificados e seja válido
            if(nodeLength > maxLength and nodeStatus=='Válida'):
                # Atualize o id do node com mais blocos
                node = seeder.id
                # Atualize o maior tamanho de blocos encontrado
                maxLength = nodeLength
                logger.info('Por enquanto o node que possui mais blocos é : ' + url + " com " + nodeLength)
        except Exception as e:
            logger.error(str(e))
            logger.warning('Node em ' + url + ' está indisponível!')

    return node, maxLength
