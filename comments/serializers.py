from rest_framework import serializers
from .models import Comment
from users.serializers import AuthorSerializer
from django.contrib.auth.hashers import make_password
import uuid
from urllib.parse import urlparse
from likes.models import PostLike
from likes.serializers import CommentLike

TEXT_MAX_LENGTH = 300
class CommentSerializer(serializers.ModelSerializer):
   type = serializers.SerializerMethodField()
   author = serializers.SerializerMethodField()
   
   class Meta:
      model = Comment
      fields = ["id","type","post","contentType","comment","author","published"]
     
   def get_author(self, obj):
      return AuthorSerializer(obj.author, context={'exclude_comments': True}).data

   def get_type(self, obj):
      return "comment"


class EditCommentSerializer(serializers.ModelSerializer):
      class Meta:
         model = Comment
         fields = '__all__'