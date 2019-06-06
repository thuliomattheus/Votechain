from rest_framework import serializers
from nodeProject.nodeApp.models import Block, Vote, Seeder
from nodeProject.nodeApp import services
import json

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        exclude = ['block']

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('__all__')

    def to_representation(self, instance):

        # Caso existam blocos inválidos
        if(services.getBlockchainSyncStatus()=="Inválida"):
            # Caso esse bloco seja inválido
            if(not services.isBlockValid(instance)):
                return {"details" : "Invalid block."}

        # Caso um bloco esteja sob validação
        elif(services.getBlockchainSyncStatus()=="Validando"):
            # Caso seja o bloco sob validação
            if(not instance.isValid()):
                return {"details" : "Validating block."}

        # Caso de blocos válidos
        representation = super(BlockSerializer, self).to_representation(instance)
        representation['votes'] = json.loads(instance.votes)
        return representation

class FullBlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('__all__')

class BlockchainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['block']

    block = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='blockDetail',
        source='index',
    )

    def to_representation(self, instance):

        # Chamada ao método herdado
        representation = super(BlockchainSerializer, self).to_representation(instance)

        # Caso a blockchain seja válida
        if(services.getBlockchainSyncStatus()=="Válida"):
            return {
                instance.__str__(): str(representation['block'])
            }

        # Caso a blockchain esteja em validação
        elif(services.getBlockchainSyncStatus()=="Validando"):
            # Caso o atual bloco seja válido
            if(instance.isValid()):
                return {
                    instance.__str__() :  str(representation['block']) + " - Valid block"
                }
            # Caso o atual bloco esteja em validação
            else:
                return {
                    instance.__str__() :  str(representation['block']) + " - Validating block"
                }

        # Caso a blockchain esteja inválida
        else:
            # Caso o atual bloco seja válido
            if(services.isBlockValid(instance)):
                return {
                    instance.__str__() :  str(representation['block']) + " - Valid block"
                }
            # Caso o atual bloco seja inválido
            else:
                return {
                    instance.__str__() :  str(representation['block']) + " - Invalid block"
                }

class LastBlockSerializer(serializers.Serializer):

    def to_representation(self, instance):

        # Se nenhum bloco for válido, retorne uma mensagem indicativa
        if(instance==-1):
            return {"details" : "Blockchain doesn't have valid blocks."}

        # Se a blockchain estiver vazia, retorne uma lista vazia
        elif(instance==0):
            return {"details" : "Blockchain is empty."}

        else:
            block = Block.objects.get(index=instance)
            return BlockSerializer(block).data

class BlockchainStatusSerializer(serializers.Serializer):
    BlockchainSize = serializers.IntegerField(source='size', label='Blocks')
    CurrentDifficulty = serializers.IntegerField(source='difficulty', label='Difficulty')
    Synchronization = serializers.CharField(source='status', label='SyncStatus')
    ConnectedNodes = serializers.IntegerField(source='connectedNodes', label='ConnectedNodes')

    def to_representation(self, instance):
        # Chamada ao método herdado
        representation = super(BlockchainStatusSerializer, self).to_representation(instance)
        # Criação de um dicionário para retornar os dados
        returnDict = {}
        # Preenchimento do dicionário
        for field in self.fields:
            returnDict[self.fields.get(field).label] = instance.get(self.fields.get(field).source)

        return returnDict


class SeederSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeder
        fields = ('ip', 'port')
