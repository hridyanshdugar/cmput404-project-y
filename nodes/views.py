from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Node
from .serializers import NodeSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@authentication_classes([IsAuthenticated])
def getNodeDetails(request):
    pk = request.query_params.get('pk', None)
    if not pk:
        return Response({"error": "Missing 'pk' query parameter"}, status=status.HTTP_400_BAD_REQUEST)
    
    node = get_object_or_404(Node, url=pk)
    return Response({"url": node.url, "username": node.username, "password": node.password}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([IsAuthenticated])
def getAllNodeDetails(request):
    nodes = Node.objects.all()
    serializer = NodeSerializer(nodes)
    
    return Response(serializer.data, status=status.HTTP_200_OK)