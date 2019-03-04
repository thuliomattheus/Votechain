from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .block import Block

""" 
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
"""

class BlockSerializer(serializers.Serializer):
    nonce = serializers.IntegerField(required=False)
    data = serializers.JSONField(required=False)
    index = serializers.IntegerField(required=False)
    previousHash = serializers.CharField(required=False)
    myHash = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Block(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance