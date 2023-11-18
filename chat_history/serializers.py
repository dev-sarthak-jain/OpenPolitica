from rest_framework import serializers
from .models import Transcript, ChatMessage, Survey

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = '__all__'

class ChatMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'