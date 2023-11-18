from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from user.models import User
from chat_history.models import Transcript,Survey
import uuid
class BaseModel(models.Model):
    eid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta: abstract = True
    # Helper method, so that we don't have to do the existence check every time.
    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            return None

class Votable(BaseModel):
    upvote_count = models.PositiveIntegerField(default=0)
    downvote_count = models.PositiveIntegerField(default=0)
    class Meta: abstract = True
class PolicyCard(Votable):
    transcript_id=models.ForeignKey(Transcript,related_name="Transcript_id",on_delete=models.CASCADE,null=True,blank=True)
    survey_id=models.ForeignKey(Survey,related_name="Survey_id",on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField()
    userneed_id = models.PositiveIntegerField()
    category = models.CharField(max_length=255)
    effective_date = models.DateTimeField()
    policy_makers = models.CharField(max_length=255)
    voting_status = models.BooleanField()
    regional_info = models.CharField(max_length=255)

    def _str_(self):
        return str(self.eid) + ": " +(self.content)


class Comment(Votable):
    post = models.ForeignKey(PolicyCard, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)  # Add the 'deleted' field
    def __str__(self):
        return str(self.eid) + ": " + self.text

class UserVote(BaseModel):
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    VOTE_TYPE = (
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote')
    )
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes', on_delete=models.CASCADE)
    #Generic Foreign Key config
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    vote_type = models.CharField(max_length=1, choices=VOTE_TYPE)
    class Meta: unique_together = ['voter', 'object_id', 'content_type']




