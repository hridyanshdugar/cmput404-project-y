import requests
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
import uuid
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from nodes.models import Node
from nodes.views import is_basicAuth, basicAuth
from requests.auth import HTTPBasicAuth

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return ContentFile(response.content)
    except requests.HTTPError as e:
        raise serializers.ValidationError(f"Error downloading image: {e}")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if "id" not in validated_data:
            validated_data["id"] = uuid.uuid4()
        else:
            validated_data["id"] = validated_data.get('id')
        validated_data['password'] = make_password(validated_data.get('password'))
        if request is not None: 
            host = request.build_absolute_uri('/') + "posts/" + str(validated_data["id"])
            referrer = request.META.get('HTTP_REFERER')
            if referrer:
                parsed_url = urlparse(referrer)
                base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
                validated_data["url"] = f'{base_url}/authors/{validated_data["id"]}'

                host_url = request.build_absolute_uri('/')
                validated_data["host"] = host_url
                
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret
     
class RemoteUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', required=False, allow_null=True)
    class Meta:
        model = User
        exclude = ('password',)
     
    def create(self, validated_data):
        validated_data['password'] = make_password(str(uuid.uuid4()))
        user_id = validated_data.get('id', None)
        if user_id:
            if User.objects.filter(id=user_id).exists():
                raise serializers.ValidationError('A user with this ID already exists.')
        
        displayName = validated_data.get('displayName')
        if User.objects.filter(displayName=displayName).exists():
            displayName += ' '  # Append a space to make the displayName unique
            validated_data['displayName'] = displayName
        
        return super().create(validated_data)

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)
        internal_data['id'] = internal_data['id'].split('/')[:-1]
        return internal_data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        id = Node.objects.get(is_self=True).url + "api/authors/" + str(data["id"])
        data["id"] = id
        return data

    class Meta:
        model = User
        fields = ["id", "host","url","type","displayName","displayName","profileImage","github","profileBackgroundImage"]
    
    def get_type(self, obj):
        return "author"