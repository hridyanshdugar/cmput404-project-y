from rest_framework import serializers
from .models import Inbox
from users.models import User
from users.serializers import AuthorSerializer
from urllib.parse import urlparse
import uuid
from comments.serializers import CommentSerializer
from comments.models import Comment
from posts.models import Post
from posts.serializers import PostSerializer
from likes.serializers import PostLikeSerializer
from followers.serializers import FollowSerializer

# Constants
TEXT_MAX_LENGTH = 300

class InboxSerializer(serializers.ModelSerializer):
     type = serializers.SerializerMethodField(read_only=True)
     posts = serializers.SerializerMethodField()
     comments = serializers.SerializerMethodField()
     author = serializers.SerializerMethodField()
     followRequest = serializers.SerializerMethodField()

     postLikes = serializers.SerializerMethodField()

     class Meta:
          model = Inbox
          fields = ["id","author", "followRequest", "comments","type","postLikes","posts"]
    
     def get_author(self, obj):
        return AuthorSerializer(obj.author, context={'exclude_comments': True}).data
     
     def get_followRequest(self, obj):
        return FollowSerializer(obj.followRequest, many=True, read_only=True).data

     def get_comments(self, obj):
        return CommentSerializer(obj.comment, many=True, read_only=True).data
     
     def get_posts(self, obj):
        return PostSerializer(obj.post, many=True, read_only=True).data
     
     def get_postLikes(self, obj):
        return PostLikeSerializer(obj.postLikes, many=True, read_only=True).data
     
     def get_type(self, obj):
        return "inbox"

