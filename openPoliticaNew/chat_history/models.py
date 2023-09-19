from django.db import models
from django.contrib.auth.models import User

class Transcript(models.Model):
    transcript_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def str(self):
        return f"{self.get_response_display()}:{self.message}"

class chat_messages(models.Model):
    chat_id=models.AutoField(primary_key=True)
    transcript_id = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    user_response=models.TextField()
    ai_response=models.TextField()
    timestamp = models.DateField(auto_now_add=True)