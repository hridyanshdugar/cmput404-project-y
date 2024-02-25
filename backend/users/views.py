from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from unione_libs.views import BaseAPIViewSet

class UsersViewPK(APIView):

     '''
     GET /users
     '''
     def get(self, request,id):
        user = get_object_or_404(User,id=id,data={"title":"No user with this id exists"})
        return user

     '''
     POST /users
     '''
     def post(self, request):
        serializer = UserSerializer(data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response("title": "Invalid Fields", "message": serializer.errors, status = status.HTTP_400_BAD_REQUEST) # Need to change the error message

class UsersView(APIView):

     '''
     GET /users
     '''
     def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     POST /users
     '''
     def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response("title": "Invalid Fields", "message": serializer.errors, status = status.HTTP_400_BAD_REQUEST)