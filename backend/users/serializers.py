from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
import uuid 

class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = '__all__'

     def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

     def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret

class AuthorSerializer(serializers.ModelSerializer):
     host = serializers.SerializerMethodField()
     url = serializers.SerializerMethodField()
     type = serializers.SerializerMethodField()
     global_id = serializers.SerializerMethodField()

     class Meta:
          model = User
          fields = ["id","global_id", "host","url","type","displayName","email","profileImage","github","profileBackgroundImage"]

     def get_host(self, obj):
        request = self.context.get('request')
        if request is not None:
            host = request.build_absolute_uri('/')
            return host
        return None
     
     def get_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            host = request.build_absolute_uri('/') + "users/" + str(obj.id)
            return host
        return None
     
     def get_global_id(self, obj):
        request = self.context.get('request')
        if request is not None:
            host = request.build_absolute_uri('/') + "users/" + str(obj.id)
            return host
        return None
     
     def get_type(self, obj):
        return "author"