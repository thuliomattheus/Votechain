from nodeProject.nodeApp.models import Block, Vote
from django.db.models.signals import post_save
from django.dispatch import receiver
from nodeProject.nodeApp import utilities
from django.utils import timezone

# Mineração do bloco
@receiver(post_save, sender=Block)
def proofOfWork(sender, instance, created, **kwargs):

    if(created):

        # Construindo uma string de zeros do tamanho da dificuldade da blockchain
        difficulty = instance.difficulty
        target = "0" * difficulty

        # Cópia do hash e do nonce do bloco atual
        # para serem realizados cálculos em memória,
        # impedindo a perda de desempenho que haveria
        # ao ficar atualizando os dados diretamente no banco
        currentHash = instance.currentBlockHash
        currentNonce = 0

        # Enquanto os 'n = difficulty' primeiros caracteres
        # do hash atual não forem iguais a zero,
        # incrementar o nonce e recalcular o hash
        while(currentHash[:difficulty] != target):
            # Atualização dos dados em memória
            currentNonce = currentNonce + 1
            currentTimestamp = timezone.now()
            currentHash = utilities.encryptSha256(
                    utilities.concatenate(
                        [
                            instance.index,
                            utilities.dateToString(currentTimestamp),
                            instance.votes,
                            instance.difficulty,
                            currentNonce,
                            instance.previousBlockHash
                        ]
                    )
                )
        instance.nonce = currentNonce
        instance.timestamp = currentTimestamp
        instance.currentBlockHash = currentHash
        instance.save()

# Verificação da validação da blockchain
def getBlockchainSyncStatus():

    blockchain = Block.objects.all()

    # Se não houverem blocos, é válida
    if(not blockchain):
        return "Válida"

    # Para todos os blocos da blockchain
    for currentBlock in blockchain:
        if(not currentBlock.isValid()):
            if(currentBlock.index == len(blockchain) and
                currentBlock.currentBlockHash=="1"*64):
                return "Validando"
            return "Inválida"
    return "Válida"

# Função para retornar a dificuldade atualizada do bloco atual
def getCurrentDifficulty():

    # Quantidade de blocos por "rodada"
    roundSize = 3

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
            if(minuteDifference < (roundSize * 3)):
                return lastBlockDifficulty + 1

            # Caso demore mais de 5 minutos por bloco
            elif(minuteDifference > (roundSize * 5)):
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
def getBlockchainStatus():
    return {
        'size' : Block.objects.count(),
        'difficulty' : getCurrentDifficulty(),
        'status' : getBlockchainSyncStatus()
    }
