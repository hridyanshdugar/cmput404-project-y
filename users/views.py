from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, AuthorSerializer
from django.shortcuts import get_object_or_404


from rest_framework.pagination import PageNumberPagination

class Pager(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

class UsersViewPK(APIView):

     '''
     GET /users
     '''
     def get(self, request,pk):
        user = get_object_or_404(User,id=pk)
        serializer = AuthorSerializer(user,context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     POST /users
     '''
     def post(self, request,pk):
        user = get_object_or_404(User,id=pk)
        serializer = UserSerializer(user,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST) # Need to change the error message
     '''
     delete /users
     '''
     def delete(self, request,pk):
        user = get_object_or_404(User,id=pk)
        user.delete()
        return Response({"title": "Successfully Deleted", "message": "User was deleted"}, status = status.HTTP_200_OK)

class UsersView(APIView):
     pagination = Pager()
     '''
     GET /users
     '''
     def get(self, request):
        users = User.objects.filter(is_superuser=False,approved=True) # No admins
        page_number = request.GET.get('page') or 1

        page = self.pagination.paginate_queryset(users, request, view=self)
        if page is not None:
            serializer = AuthorSerializer(page,many=True,context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

     '''
     POST /users
     '''
     def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)