import requests
from rest_framework import serializers

from nodes.models import Node
from .models import Post
from users.models import User
from users.serializers import AuthorSerializer
from urllib.parse import urlparse
import uuid
from comments.serializers import CommentSerializer
from comments.models import Comment

# Constants
TEXT_MAX_LENGTH = 300
VISIBILITY_CHOICES = [(1, "PUBLIC"), (2, "FRIENDS"), (3, "UNLISTED")]

class PostEditSerializer(serializers.ModelSerializer):
     class Meta:
          model = Post
          fields = ["content","contentType","visibility","description"]

class RemotePostSerializer(serializers.ModelSerializer):
     class Meta:
          model = Post
          fields = ["id", "host", "origin", "source","content","contentType","published","visibility","description", "author"]


class PostSerializer(serializers.ModelSerializer):
     type = serializers.SerializerMethodField(read_only=True)
     commentsSrc = serializers.SerializerMethodField()
     comments = serializers.SerializerMethodField()
     author = serializers.SerializerMethodField()
     count = serializers.SerializerMethodField()

     class Meta:
          model = Post
          fields = ["id", "title", "host", "origin", "source", "type", "content","contentType","published","comments","commentsSrc","visibility", "description", "author","count"]

     def __init__(self, *args, **kwargs):
        exclude_comments = False
        if 'context' in kwargs and 'exclude_comments' in kwargs['context']:
            exclude_comments = kwargs['context'].get('exclude_comments', False)
        super(PostSerializer, self).__init__(*args, **kwargs)
        if exclude_comments:
            self.fields.pop('commentsSrc', None)
    
     def get_author(self, obj):
        return AuthorSerializer(obj.author, context={'exclude_comments': True}).data

     def get_commentsSrc(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializer(comments, many=True, read_only=True).data
   

     def create(self, validated_data):
        request = self.context.get('request')
        print("hi 1")
        validated_data["id"] = uuid.uuid4()
        if request is not None: 
            print("hi 12", validated_data)
            #     "origin":"<http://domain_z>/api/authors/<author_id_z>/posts/<post_id_z>",
            origin = Node.objects.get(is_self=True).url + "api/authors/" + str(validated_data["author"]["id"]) + "/posts/" + str(validated_data["id"])
            validated_data["origin"] = origin
            print("hi 13")
            if "source" not in validated_data:
                  validated_data["source"] = origin
            print("hi 14")
            validated_data["host"] = request.build_absolute_uri('/')
            print("hi 15")
        return super().create(validated_data)
     
     def get_type(self, obj):
        return "post"

     def get_comments(self, obj):
        request = self.context.get('request')
        if request is not None:
            host = request.build_absolute_uri('/') + "posts/" + str(obj.id) + "/comments/"
            return host
        return None
     
     def get_count(self, obj):
         return len(Comment.objects.filter(post=obj))
