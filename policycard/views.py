from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .serializers import *


class PostListView(APIView):
    def get(self, request):
        posts = PolicyCard.objects.all().order_by('-date_created')
        serializer = PolicyCardSerializer(posts, many=True)  # Use your serializer to serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_post = PolicyCardSerializer(data=request.data)
        if serialized_post.is_valid():
            serialized_post.save()
            return Response(serialized_post.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_post.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PostView(APIView):
    def get(self, request, eid):  # Change 'post_id' to 'eid'
        post = get_object_or_404(PolicyCard, eid=eid)  # Change 'post_id' to 'eid'
        serializer = PolicyCardSerializer(post)  # Use your serializer to serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, eid):
        post = get_object_or_404(PolicyCard, eid=eid)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
   
class PostCommentsView(APIView):
    def get(self, request, eid):  # Change 'post_id' to 'eid'
        post = get_object_or_404(PolicyCard, eid=eid)  # Change 'post_id' to 'eid'
        comments = Comment.objects.filter(post=post).order_by('-date_created')  # Use 'post' instead of 'post_id'
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, eid):
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_comment.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    def delete(self, request, eid):
        comment = get_object_or_404(Comment, eid=eid)
        comment.deleted = True  # Mark the comment as deleted
        comment.save()  # Save the updated comment
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, eid):
        comment = get_object_or_404(Comment, eid=eid)
        new_text = request.data.get('text')
        if new_text is not None:
            # Update the comment's text with the new text
            comment.text = new_text
            comment.save()  # Save the updated comment
            # Serialize and return the updated comment
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'detail': 'New text not provided in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

