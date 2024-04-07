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
          fields = ["id", "origin", "source","content","contentType","published","visibility","description", "author"]


class PostSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    commentsSrc = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def to_internal_value(self, data):
        print("fat stacks1", data)
        internal_data = super().to_internal_value(data)
        internal_data['id'] = internal_data.get('id', "").split('/')[-1]
        print("fat stacks", internal_data)
        return internal_data
    
    def to_representation(self, instance):
        print("fat stacks4", instance)
        data = super().to_representation(instance)
        print("fat stacks3", data)
        data["id"] = data["origin"]
        print("fat stacks5", data)
        return data

    class Meta:
        model = Post
        fields = ["id", "title", "origin", "source", "type", "content","contentType","published","comments","commentsSrc","visibility", "description", "author","count"]

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
        print("hi 12", validated_data)
        #     "origin":"<http://domain_z>/api/authors/<author_id_z>/posts/<post_id_z>",
        origin = Node.objects.get(is_self=True).url + "api/authors/" + str(validated_data["author"].id) + "/posts/" + str(validated_data["id"])
        print("hi 13", origin)
        validated_data["origin"] = origin
        if "source" not in validated_data:
                validated_data["source"] = origin
        print("hi 14")
        return super().create(validated_data)
    
    def get_type(self, obj):
        return "post"

    def get_comments(self, obj):
        return obj.origin + "/comments"
    
    def get_count(self, obj):
        return len(Comment.objects.filter(post=obj))
