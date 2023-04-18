from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ChatbotClient, Client, ClientPhone, ClientSymptomQuestionAnswer, Stage, SymptomQuestion


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ['url', 'name']


class ChatbotClientSerializer(serializers.ModelSerializer):

    client = serializers.SlugRelatedField(queryset=Client.objects.all(),slug_field='id')

    class Meta:
        model = ChatbotClient
        fields = ['url', 'id', 'social_media_id', 'social_media_name', 'client']


class ClientSymptomQuestionAnswerSerializer(serializers.ModelSerializer):

    question = serializers.SlugRelatedField(queryset=SymptomQuestion.objects.all(),slug_field='id')
    client = serializers.SlugRelatedField(queryset=Client.objects.all(),slug_field='id')
    stage = serializers.SlugRelatedField(queryset=Stage.objects.all(),slug_field='id')

    class Meta:
        model = ClientSymptomQuestionAnswer
        fields = ['id', 'question', 'client', 'answer', 'stage']


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['url', 'id', 'type', 'gender', 'age_range']


class ClientPhoneSerializer(serializers.ModelSerializer):

    client = serializers.SlugRelatedField(queryset=Client.objects.all(),slug_field='id')

    class Meta:
        model = ClientPhone
        fields = ['url', 'phone_number', 'phone_type', 'client']


# class ClientSymptomQuestionAnswerBulkCreateUpdateSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         csqa_data = [ClientSymptomQuestionAnswer(**item) for item in validated_data]
#         return ClientSymptomQuestionAnswer.objects.bulk_create(csqa_data)

# class ClientCreateSerializer(serializers.ModelSerializer):
#     """
#     Serializer to Add Client together with ChatbotClient
#     """

#     class ChatbotClientTempSerializer(serializers.HyperlinkedModelSerializer):
#         class Meta:
#             model = ChatbotClient
#             # 'model_a_field' is a FK which will be assigned after creation of 'Client' model entry
#             # First entry of ChatbotClient will have (default) fieldB3 value as True, rest as False
#             # 'field4' will be derived from its counterpart from the 'Product' model attribute
#             exclude = ['client_id']

#     chatbot_client = ChatbotClientTempSerializer()

#     class Meta:
#         model = Client
#         fields = ['url', 'type', 'gender', 'age_range', 'social_media_id', 'social_media_name']

#     def create(self, validated_data):
#         chatbot_client_data = validated_data.pop('chatbot_client')
#         client_instance = Client.objects.create(**validated_data)
#         ChatbotClient.objects.create(client_id=client_instance,**chatbot_client_data)
#         return client_instance
