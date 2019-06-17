from rest_framework import serializers
from clientProject.clientApp import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields = '__all__'

class SeederSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seeder
        fields = '__all__'
