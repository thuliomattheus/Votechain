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
    # Método para alterar o formato dos votos de string para json
    def to_representation(self, instance):
        # Chamada ao método original da super classe
        representation = super(BlockSerializer, self).to_representation(instance)
        # Sobrescrita do método padrão para mostrar os votos formatados como json
        representation['votes'] = json.loads(instance.votes)
        return representation

    class Meta:
        model = Block
        fields = ('__all__')

class InfoChainSerializer(serializers.Serializer):
    depth = serializers.IntegerField()
    difficulty = serializers.IntegerField()