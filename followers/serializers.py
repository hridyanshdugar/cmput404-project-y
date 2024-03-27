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
from likes.serializers import CommentLikeSerializer, PostLikeSerializer
from .models import FollowStatus

# Constants
TEXT_MAX_LENGTH = 300

class FollowSerializer(serializers.ModelSerializer):
   actor = serializers.SerializerMethodField()
   obj = serializers.SerializerMethodField()
   class Meta:
         model = FollowStatus
         fields = '__all__'
      
   def get_actor(self, obj):
        return AuthorSerializer(obj.actor, context={'exclude_comments': True}).data
   
   def get_obj(self, obj):
        return AuthorSerializer(obj.obj, context={'exclude_comments': True}).data

