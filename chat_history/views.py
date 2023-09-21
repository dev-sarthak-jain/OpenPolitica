from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Transcript, ChatMessage
from .serializers import TranscriptSerializer, ChatMessagesSerializer

def llm_response(user_response: str) -> str:
    # Replace this with your actual AI response generation logic
    # For now, it echoes the user's input
    ai_response = f"Hello, you said: {user_response}"
    return ai_response

@api_view(['GET'])
def allTranscripts(request, user_id):
    # Retrieve all transcripts for the given user
    user_transcripts = Transcript.objects.filter(user_id=user_id)
    
    # Serialize and return the transcripts
    serializer = TranscriptSerializer(user_transcripts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST', 'DELETE'])
def create_messages(request, transcript_id):
    # Get the transcript object or return a 404 if not found
    transcript = get_object_or_404(Transcript, pk=transcript_id)
    
    if request.method == 'GET':
        # Retrieve all messages of a particular transcript
        user_messages = ChatMessage.objects.filter(transcript=transcript_id)
        # Serialize and return the messages
        serializer = ChatMessagesSerializer(user_messages, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Extract user_response from the request data (adjust based on your request structure)
        user_response = request.data.get('user_response')

        # Generate AI response based on user input
        ai_response = llm_response(user_response)

        # Create a new ChatMessage
        chat_message = ChatMessage.objects.create(
            transcript=transcript_id,
            user_response=user_response,
            ai_response=ai_response
        )
        chat_message.save()
        # Serialize and return the created chat message with a 201 status code
        serializer = ChatMessagesSerializer(chat_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        transcript = get_object_or_404(Transcript, pk=transcript_id)
        transcript.delete()
        return Response({"message": "Transcript deleted successfully"})

    # Return a 404 status code and message when data doesn't match
    return Response({
        "message": "Data doesn't match"
    }, status=status.HTTP_404_NOT_FOUND)

class Transcription(APIView):
    def post(self, request):
        serialized_transcript = TranscriptSerializer(data=request.data)
        if serialized_transcript.is_valid():
            serialized_transcript.save()
            return Response(serialized_transcript.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_transcript.errors, status=status.HTTP_400_BAD_REQUEST)




    # class transciption_api(APIView):
#     def POST(request, self):
#         if request.method == 'POST':
#             print("requested data",request.data)
#             # Extract the user_response from the request data
#             # user_response = request.data.get('user_response')

#             # Create a new Transcript object
#             serializer = TranscriptSerializer(request.data)
#             print(serializer)
#             if(TranscriptSerializer.is_valid()):
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 print("Validation Error")
#                 return Response(serializer.errors)

#             # Serialize and return the created transcript with a 201 status code
#         #     return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # # Return a 400 status code and message when the request method is not POST
#     # return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)