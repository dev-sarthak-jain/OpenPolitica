from django.urls import path
from . import views


urlpatterns = [
    path("all-transcripts/<int:user_id>/", views.AllTranscripts.as_view(), name="all-transcripts"),
    path("create-messages/<transcript_id>/", views.CreateMessages.as_view(), name="create-messages"),
    path("transcription/", views.Transcription.as_view(), name="transcription"),
    path('generate-update-title/<uuid:transcript_id>/', views.GenerateUpdateTitle.as_view(), name='generate-update-title'),
    path("all-messages/",views.ChatMessageList.as_view(), name = "ALL messages"),
    path('surveys/<int:user_id>/<uuid:transcript_id>', views.SurveyAPIView.as_view(), name='user-surveys'),
    path('surveys/<uuid:survey_id>/update', views.SurveyUpdateApiView.as_view(), name='survey-update'),
    path('policycardgeneration/<uuid:survey_id>/<uuid:transcript_id>', views.PolicyCardApiView.as_view(), name='policard-creation'),
]


