from rest_framework import serializers
from nodeProject.nodeApp.models import Block, Vote
from nodeProject.nodeApp import utilities
import json
from datetime import datetime

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('voterPubKey', 'candidateRole', 'candidateNumber', 'digitalSignature')

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('__all__')

    # Método para alterar o formato dos votos de string para json
    def to_representation(self, instance):
        # Chamada ao método original da super classe
        representation = super(BlockSerializer, self).to_representation(instance)
        # Sobrescrita do método padrão para mostrar os votos formatados como json
        representation['votes'] = json.loads(instance.votes)
        return representation

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
        representation = super(BlockchainSerializer, self).to_representation(instance)
        return {
            instance.__str__(): representation['block']
        }

class BlockchainStatusSerializer(serializers.Serializer):
    Depth = serializers.IntegerField(source='depth')
    Difficulty = serializers.IntegerField(source='difficulty')
    Status = serializers.CharField(source='status')