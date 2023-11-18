from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Transcript, ChatMessage, Survey
from user.models import User
from .serializers import TranscriptSerializer, ChatMessagesSerializer, SurveySerializer
from .Func1_chatResponse import generate_response
from .Func2_userneedextractor import UserNeedsExtractor
from .Func3_policy import generate_policy_card
from .Func4_titleGeneration import generate_chat_title
from policycard.models import PolicyCard
from policycard.serializers import PolicyCardSerializer

def llm_response(user_response: str) -> str:
    # Replace this with your actual AI response generation logic
    # For now, it echoes the user's input
    ai_response = f"Hello, you said: {user_response}"
    return ai_response

class Transcription(APIView):
    def post(self, request):
        serialized_transcript = TranscriptSerializer(data=request.data)
        if serialized_transcript.is_valid():
            serialized_transcript.save()
            return Response(serialized_transcript.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_transcript.errors, status=status.HTTP_400_BAD_REQUEST)

class AllTranscripts(APIView):
    def get(self, request, user_id):
        # Retrieve all transcripts for the given user
        user_transcripts = Transcript.objects.filter(user_id=user_id)
        
        # Serialize and return the transcripts
        serializer = TranscriptSerializer(user_transcripts, many=True)
        return Response(serializer.data)


class GenerateUpdateTitle(APIView):
    def post(self, request, transcript_id):
        # Get the transcript object or return a 404 if not found
        transcript = get_object_or_404(Transcript, transcript_id=transcript_id)
        # Extract the title from the request data (assuming it's provided by the frontend)
        provided_title = request.data.get('title')
        # Generate a new title using your custom function (replace with your actual logic)
        generated_title = generate_chat_title(provided_title)
        # Update the transcript with the new title
        transcript.title = generated_title
        transcript.save()
        serializer = TranscriptSerializer(transcript)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, transcript_id):
        # Get the transcript object or return a 404 if not found
        transcript = get_object_or_404(Transcript, transcript_id=transcript_id)
        
        # Extract the new title from the request data
        new_title = request.data.get('title')

        # Update the title and save the transcript
        transcript.title = new_title
        transcript.save()

        # Return a response indicating success
        return Response({"message": "Transcript title updated successfully"}, status=status.HTTP_200_OK)


class CreateMessages(APIView):
    def get(self, request, transcript_id):
        # Get the transcript object or return a 404 if not found
        transcript = get_object_or_404(Transcript, pk=transcript_id)
        
        # Retrieve all messages of a particular transcript
        user_messages = ChatMessage.objects.filter(transcript=transcript_id)
        
        
        # Serialize and return the messages
        serializer = ChatMessagesSerializer(user_messages, many=True)
        return Response(serializer.data)

    def post(self, request, transcript_id):
        # Get the transcript object or return a 404 if not found
        transcript = get_object_or_404(Transcript, pk=transcript_id)
        
        messages = ChatMessage.objects.filter(transcript=transcript_id).order_by('timestamp')
        message_data = [{"user":message.user_response,"AI":message.ai_response} for message in messages]

        
        # Extract user_response from the request data (adjust based on your request structure)
        user_response = request.data.get('user_response')
        user_id = request.data.get('user')
        user = get_object_or_404(User, id=user_id)
        # Generate AI response based on user input
        ######ai_response = llm_response(user_response)
        ai_response = generate_response(user_response, message_data)

        chat_message = ChatMessage.objects.create(
            transcript=transcript,
            user=user,
            user_response=user_response,
            ai_response=ai_response
        )
        chat_message.save()
        serializer = ChatMessagesSerializer(chat_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, transcript_id):
        transcript = get_object_or_404(Transcript, pk=transcript_id)
        transcript.delete()
        return Response({"message": "Transcript deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ChatMessageList(APIView):
    def get(self, request):
        queryset = ChatMessage.objects.all()
        serializer = ChatMessagesSerializer(queryset, many = True)
        return Response(serializer.data)
    

class SurveyAPIView(APIView):
    def post(self, request):
        serialized_survey = SurveySerializer(data=request.data)
        if serialized_survey.is_valid():
            serialized_survey.save()
            return Response(serialized_survey.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_survey.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
   
        
    
    def get(self, request, user_id, transcript_id):
        # Get the transcript object
        transcript = get_object_or_404(Transcript, pk=transcript_id)
        Survey.objects.filter(transcript=transcript).delete()

        # Retrieve all chat messages associated with the transcript
        messages = ChatMessage.objects.filter(transcript=transcript).order_by('timestamp')

        # Construct the chat transcript in the required format
        chat_transcript = []
        for message in messages:
            chat_transcript.append({"role": "user", "content": message.user_response})
            chat_transcript.append({"role": "assistant", "content": message.ai_response})

        extractor = UserNeedsExtractor()
        structured_needs, survey = extractor.run(chat_transcript)
        print(survey)

        # Update the questions in the survey
        survey['questions'] = "rank these user needs"

        # Create the survey data
        survey_data = {
            "user": user_id,
            "transcript": transcript_id,
            "questions": survey['questions'],
            "user_needs": len(structured_needs),
            "options": survey['options']
        }

        # Save the survey data and return it in the response
        serializer = SurveySerializer(data=survey_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyUpdateApiView(APIView):
    
    def patch(self, request, survey_id):
        survey = get_object_or_404(Survey, pk=survey_id)
        new_options = request.data.get('options')

        if new_options is not None:
            if not isinstance(new_options, list):
                return Response({'detail': 'Invalid data format for options. Expected a list.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the survey options
            survey.options = new_options
            survey.save()

            # Serialize and return the updated survey
            serializer = SurveySerializer(survey)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'detail': 'New options not provided in the request data.'}, status=status.HTTP_400_BAD_REQUEST)


class PolicyCardApiView(APIView):
    
    def get(self, request, survey_id, transcript_id):
        survey = get_object_or_404(Survey, pk=survey_id)
        
        
        data = {}
        for i in survey.options:
            data[i[0]] = i[1]
            
        policy_cards = generate_policy_card(data)
        
        # Assuming generate_policy_card returns a list of dictionaries
        generated_policy_cards = []
        for policy_card_data in policy_cards:
            # Add the survey_id and transcript_id to the policy card data
            policy_card_data['survey_id'] = survey_id
            policy_card_data['transcript_id'] = transcript_id
            
            # Assuming you have a serializer for PolicyCard
            serializer = PolicyCardSerializer(data=policy_card_data)
            if serializer.is_valid():
                policy_card = serializer.save()
                generated_policy_cards.append(PolicyCardSerializer(policy_card).data)
            else:
                # If there's an error in serialization, you can handle it accordingly
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Policy cards generated successfully", "policy_cards": generated_policy_cards}, status=status.HTTP_201_CREATED)