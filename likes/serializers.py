from rest_framework import serializers
from .models import CommentLike, PostLike
from users.models import User
from users.serializers import AuthorSerializer
from urllib.parse import urlparse
import uuid
from comments.serializers import CommentSerializer
from comments.models import Comment

# Constants
TEXT_MAX_LENGTH = 300

class PostLikeSerializer(serializers.ModelSerializer):
      type = serializers.SerializerMethodField(read_only=True)
      class Meta:
         model = PostLike
         fields = ["summary","type", "author"]
      
      def get_author(self, obj):
         return AuthorSerializer(obj.author, context={'exclude_comments': True}).data
      
      def get_type(self, obj):
        return "Like"

class EditPostLikeSerializer(serializers.ModelSerializer):
      class Meta:
         model = PostLike
         fields = '__all__'

class CommentLikeSerializer(serializers.ModelSerializer):
      type = serializers.SerializerMethodField(read_only=True)
      class Meta:
         model = CommentLike
         fields = ["summary","type", "author", "comment"]
      
      def get_author(self, obj):
         return AuthorSerializer(obj.author, context={'exclude_comments': True}).data
      
      def get_type(self, obj):
        return "Like"
      
class EditCommentLikeSerializer(serializers.ModelSerializer):
      class Meta:
         model = CommentLike
         fields = '__all__'