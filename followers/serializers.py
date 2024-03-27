from rest_framework import serializers
from users.serializers import AuthorSerializer
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


class SaveFollowSerializer(serializers.ModelSerializer):
   class Meta:
         model = FollowStatus
         fields = '__all__'