from rest_framework import serializers
from .models import Inbox
from users.models import User
from users.serializers import AuthorSerializer
from urllib.parse import urlparse
import uuid
from comments.serializers import CommentSerializer
from comments.models import Comment

# Constants
TEXT_MAX_LENGTH = 300
VISIBILITY_CHOICES = [(1, "PUBLIC"), (2, "FRIENDS"), (3, "UNLISTED")]

class InboxSerializer(serializers.ModelSerializer):
     url = serializers.SerializerMethodField()
     type = serializers.SerializerMethodField(read_only=True)
     commentsSrc = serializers.SerializerMethodField()
     comments = serializers.SerializerMethodField()
     author = serializers.SerializerMethodField()
     count = serializers.SerializerMethodField()

     class Meta:
          model = Inbox
          fields = ["id","global_id", "host","url","type","content","contentType","published","comments","commentsSrc","visibility","origin","description", "author","count"]

     def __init__(self, *args, **kwargs):
        exclude_comments = False
        if 'context' in kwargs and 'exclude_comments' in kwargs['context']:
            exclude_comments = kwargs['context'].get('exclude_comments', False)
        super(InboxSerializer, self).__init__(*args, **kwargs)
        if exclude_comments:
            self.fields.pop('commentsSrc', None)
    
     def get_author(self, obj):
        return AuthorSerializer(obj.author, context={'exclude_comments': True}).data

     def get_commentsSrc(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializer(comments, many=True, read_only=True).data
     
     def get_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            host = request.build_absolute_uri('/') + "posts/" + str(obj.id)
            return host
        return None

     def create(self, validated_data):
        request = self.context.get('request')
        validated_data["id"] = uuid.uuid4()
        if request is not None: 
            host = request.build_absolute_uri('/') + "posts/" + str(validated_data["id"])
            referrer = request.META.get('HTTP_REFERER')
            if referrer:
                parsed_url = urlparse(referrer)
                base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
                validated_data["origin"] = f'{base_url}/posts/{validated_data["id"]}'
            validated_data["global_id"] = host
            validated_data["host"] = request.build_absolute_uri('/')
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
