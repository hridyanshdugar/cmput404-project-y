from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
import re


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