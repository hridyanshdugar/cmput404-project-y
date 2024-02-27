from rest_framework import serializers
from .models import Post

# Constants
TEXT_MAX_LENGTH = 300
VISIBILITY_CHOICES = [(1, "PUBLIC"), (2, "FRIENDS"), (3, "UNLISTED")]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Post` instance, given the validated data
        """
        return Post.object.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Post` instance, given the validated data
        """
        instance.title = validated_data.get('title', instance.title)
        instance.id = validated_data.get('id', instance.id) 
        instance.source = validated_data.get('source', instance.source)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.description = validated_data.get('description', instance.description)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.published = validated_data.get('published', instance.published)
        instance.visibility = validated_data.get('visibility', instance.visibility)

        instance.save()
        
        return instance

    def delete(self, instance):
        """
        Delete and return an existing `Post` instance, given the validated data
        """
        instance.delete()
        return instance