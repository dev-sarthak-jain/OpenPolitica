from rest_framework import generics
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Transcript, chat_messages
from .serializers import TranscriptSerializer, ChatMessagesSerializer
from rest_framework.views import APIView


@api_view()
def allTranscripts(request,user_id):
    user_transcripts = get_object_or_404(Transcript, pk = user_id)
    serializer = TranscriptSerializer(user_transcripts)
    return Response(serializer.data)

@api_view(['POST'])
def create_messages(request,transcript_id):
    if request.method == 'POST':
        serializer=ChatMessagesSerializer(data=request.data)
        #function chat response
        return Response("ok")





    return Response({
        "message":"data create"
    })