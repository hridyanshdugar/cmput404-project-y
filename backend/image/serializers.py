from rest_framework import serializers
from .models import Image
from django.contrib.auth.hashers import make_password
import uuid
from urllib.parse import urlparse


class ImageSerializer(serializers.ModelSerializer):
     class Meta:
          model = Image
          fields = '__all__'
