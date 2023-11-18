from rest_framework import serializers
from .models import PolicyCard, Comment, UserVote

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PolicyCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyCard
        fields='__all__'

class UserVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVote
        fields = '__all__'

