from rest_framework import serializers
from .models import Transcript
from .models import chat_messages


class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = '__all__'
        

class ChatMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = chat_messages
        fields = '__all__'
