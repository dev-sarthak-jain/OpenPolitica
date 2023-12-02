from django.db import models
from user.models import User
import uuid

class Transcript(models.Model):
    transcript_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcript {self.transcript_id} by {self.user.username}"


class ChatMessage(models.Model):
    chat_id = models.AutoField(primary_key=True)
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Specify a default value
    user_response = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Message {self.chat_id}"

class Survey(models.Model):
    survey_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    questions = models.CharField(max_length=255)
    user_needs = models.IntegerField()
    options = models.JSONField()
    survey_updated=models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Survey {self.survey_id}"