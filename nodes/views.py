from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Node
from .serializers import NodeSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from base64 import b64decode

@api_view(['GET'])
@authentication_classes([IsAuthenticated])
def getNodeDetails(request):
    """
    Get node details
    """
    pk = request.query_params.get('pk', None)
    if not pk:
        return Response({"error": "Missing 'pk' query parameter"}, status=status.HTTP_400_BAD_REQUEST)
    
    node = get_object_or_404(Node, url=pk)
    return Response({"url": node.url, "username": node.username, "password": node.password}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([IsAuthenticated])
def getAllNodeDetails(request):
    """
    Get all the node details
    """
    nodes = Node.objects.all()
    serializer = NodeSerializer(nodes)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

def is_basicAuth(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return False

    auth_type, _ = auth_header.split(' ', 1)
    if auth_type.lower() != 'basic':
        return False
    else:
        return True

def basicAuth(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    print(auth_header)
    if not auth_header:
        return False
    
    # request_url = request.META.get('HTTP_HOST')
    auth_type, encoded_credentials = auth_header.split(' ', 1)
    if auth_type.lower() != 'basic':
        return False

    decoded_credentials = b64decode(encoded_credentials).decode('utf-8')
    username, password = decoded_credentials.split(':', 1)
    # print("SENT BY: ",request_url)
    if Node.objects.filter(username=username,password=password).exists():
        return True
    else:
        return False