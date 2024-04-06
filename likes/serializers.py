from rest_framework import serializers
from .models import PostLike
from users.models import User
from users.serializers import AuthorSerializer
from urllib.parse import urlparse
import uuid
from comments.serializers import CommentSerializer
from comments.models import Comment
from users.serializers import AuthorSerializer

# Constants
TEXT_MAX_LENGTH = 300

class PostLikeSerializer(serializers.ModelSerializer):
      type = serializers.SerializerMethodField(read_only=True)
      author = serializers.SerializerMethodField
      object = serializers.SerializerMethodField
      class Meta:
         model = PostLike
         fields = ["summary","type", "author", "object"]
      
      def get_author(self, obj):
         return AuthorSerializer(obj.author, context={'exclude_comments': True}).data
      
      def get_type(self, obj):
        return "Like"
      
      def get_object(self, obj):
         return obj.post

class EditPostLikeSerializer(serializers.ModelSerializer):
      object = serializers.SerializerMethodField
      author = serializers.SerializerMethodField
      type = serializers.SerializerMethodField

      class Meta:
         model = PostLike
         fields = '__all__'

      def get_object(self, obj):
         return obj.post
      
      def get_author(self, obj):
         return AuthorSerializer(obj.author, context={'exclude_comments': True}).data
      
      def get_type(self, obj):
        return "Like"
      