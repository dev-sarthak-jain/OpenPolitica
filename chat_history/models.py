from django.db import models
from django.contrib.auth.models import User

class Transcript(models.Model):
    transcript_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcript {self.transcript_id}"

class ChatMessage(models.Model):
    chat_id = models.AutoField(primary_key=True)
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    user_response = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Message {self.chat_id}"
