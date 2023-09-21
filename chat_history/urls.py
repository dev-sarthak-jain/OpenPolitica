from django.urls import path
from . import views

urlpatterns = [
    path('api/transcripts/<int:user_id>/', views.allTranscripts, name='all-transcripts'),
    path('api/transcripts/<int:transcript_id>/', views.create_messages, name='create-messages'),
    path('api/transcriptions/', views.Transcription.as_view(), name='transcription-list'),
]
