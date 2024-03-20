from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
import uuid
from urllib.parse import urlparse


class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = '__all__'

     def create(self, validated_data):
        request = self.context.get('request')
        validated_data["id"] = uuid.uuid4()
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
                
            validated_data["global_id"] = host
        return super().create(validated_data)

     def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret
     
class RemoteUserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          exclude = ('password',)
     
     def create(self, validated_data):
        validated_data['password'] = make_password(uuid.uuid4())
        
        return super().create(validated_data)

class AuthorSerializer(serializers.ModelSerializer):
     type = serializers.SerializerMethodField()

     class Meta:
          model = User
          fields = ["id","global_id", "host","url","type","displayName","email","profileImage","github","profileBackgroundImage"]
     
     def get_type(self, obj):
        return "author"