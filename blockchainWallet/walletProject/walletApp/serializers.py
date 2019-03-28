from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .block import Block
from .models import Usuario

""" 
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ('url', 'username', 'email', 'groups')
"""

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'