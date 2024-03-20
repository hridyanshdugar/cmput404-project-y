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
   author = AuthorSerializer(read_only=True)
   likes = serializers.SerializerMethodField()
   
   class Meta:
      model = Comment
      fields = ["id","global_id","type","post","contentType","comment","author","published","likes"]

   def create(self, validated_data):
      request = self.context.get('request')
      validated_data["id"] = uuid.uuid4()
      if request is not None: 
         host = request.build_absolute_uri('/') + "comments/" + str(validated_data["id"])
         validated_data["global_id"] = host
      return super().create(validated_data)
     
   def get_author(self, obj):
      return AuthorSerializer(obj.author, context={'exclude_comments': True}).data

   def get_type(self, obj):
      return "comment"
   
   def get_likes(self, obj):
      return len(CommentLike.objects.filter(comment=obj))