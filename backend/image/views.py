from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Image
from .serializers import ImageSerializer
from django.shortcuts import get_object_or_404


class ImageViewPK(APIView):

     '''
     GET /images
     '''
     def get(self, request,pk):
        image = get_object_or_404(Image,image=pk)
        serializer = ImageSerializer(image,context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     POST /images
     '''
     def post(self, request,pk):
        image = get_object_or_404(Image,image=pk)
        serializer = ImageSerializer(image,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
     
     '''
     delete /images
     '''
     def delete(self, request,pk):
        user = get_object_or_404(Image,image=pk)
        user.delete()
        return Response({"title": "Successfully Deleted", "message": "User was deleted"}, status = status.HTTP_200_OK)

class ImageView(APIView):
     
     '''
     POST /images
     '''
     def post(self, request):
        serializer = ImageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)