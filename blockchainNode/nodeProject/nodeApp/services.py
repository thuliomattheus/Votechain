from nodeProject.nodeApp.models import Block, Vote
from django.db.models.signals import post_save
from django.dispatch import receiver
from nodeProject.nodeApp import utilities

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
            currentHash = utilities.encryptSha256(
                    utilities.concatenate(
                        [
                            instance.index,
                            utilities.dateToString(instance.timestamp),
                            instance.votes,
                            instance.difficulty,
                            currentNonce,
                            instance.previousBlockHash
                        ]
                    )
                )
        instance.nonce = currentNonce
        instance.currentBlockHash = currentHash
        instance.save()

# Verificação da validação da blockchain
def isChainValid():

    blockchain = Block.objects.all()

    # Se não houverem blocos, não é válida
    if(not blockchain):
        return True

    # Para todos os blocos da blockchain
    for index, currentBlock in enumerate(blockchain):

        # Construindo uma string de zeros do tamanho da dificuldade da blockchain
        target = "0"*currentBlock.difficulty

        # Hash correto do bloco
        realHash = utilities.encryptSha256(utilities.concatenate(currentBlock.getAttributesAsList()))

        # Caso Geral:
        #   Caso o hash do bloco seja diferente do que deveria ser
        #   Ou
        #   Caso o hash do bloco não tenha sido validado pelo PoW
        if(currentBlock.currentBlockHash != realHash or
            currentBlock.currentBlockHash[:currentBlock.difficulty] != target):
            print("ERRO 1")
            print("currentBlockHash = " + currentBlock.currentBlockHash)
            print("realHash = " + realHash)
            return False

        # Caso específico do bloco genesis:
        if(index==0):
            if(currentBlock.previousBlockHash != "0"*64):
                print("ERRO 2")
                return False
        # Caso específico dos outros blocos:
        else:
            previousBlock = Block.objects.get(index=index)
            # Caso o previousHash do bloco atual seja diferente do hash do bloco anterior
            if(currentBlock.previousBlockHash != previousBlock.currentBlockHash):
                print("ERRO 3")
                return False

    return True

# Função para retornar a dificuldade atualizada do bloco atual
def getCurrentDifficulty():

    # Tamanho atual da blockchain
    blockchainLength = Block.objects.count()

    # Dificuldade inicial
    if(blockchainLength==0):
        return 4
    # A cada 5 blocos, atualizar a dificuldade da nova "rodada" de 5 blocos
    elif(blockchainLength%5==0):

        firstRoundIndex = blockchainLength/5
        firstRoundBlock = Block.objects.get(index=5*firstRoundIndex)
        lastRoundBlock = Block.objects.get(index=blockchainLength)

        # Caso demore menos de 5 minutos pra minerar todos os blocos da rodada (5 blocos)
        if(lastRoundBlock.timestamp.minute - firstRoundBlock.timestamp.minute < 5):
            return lastRoundBlock.difficulty + 1
        # Caso demore mais de 30 minutos pra minerar todos os blocos da rodada (5 blocos)
        elif(lastRoundBlock.timestamp.minute - firstRoundBlock.timestamp.minute > 30):
            return lastRoundBlock.difficulty - 1
        # Casos de valores aceitáveis, não altera a dificuldade
        else:
            return lastRoundBlock.difficulty

    # Repete a dificuldade anterior
    else:
        return Block.objects.get(index=blockchainLength).difficulty
