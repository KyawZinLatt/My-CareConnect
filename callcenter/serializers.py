from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ChatbotClientDemo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ChatbotClientDemoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatbotClientDemo
        fields = ['url', 'social_media_id', 'social_media_name','gender','age_range']