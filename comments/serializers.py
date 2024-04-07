from rest_framework import serializers

from nodes.models import Node
from .models import Comment
from users.serializers import AuthorSerializer

TEXT_MAX_LENGTH = 300
class CommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)
        internal_data['id'] = internal_data['id'].split('/')[:-1]
        return internal_data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # http://127.0.0.1:5454/authors/<author_id>/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
        data["id"] = Node.objects.get(is_self=True).url + "api/authors/" + str(data["author"].id) + "/posts/" + str(data["post"]) + "/comments/" + str(data["id"])
        return data

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