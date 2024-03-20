from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Inbox, Post
from rest_framework.pagination import PageNumberPagination
from posts.serializers import PostSerializer, PostEditSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import RemoteUserSerializer
from posts.serializers import RemotePostSerializer
import requests
from requests.exceptions import JSONDecodeError

class Pager(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

# Create your views here.
class InboxView(APIView):
     pagination = Pager()

     '''
     GET /authors/{id}/inbox
     '''
     def get(self, request, pk):
        print(pk)
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     PUT /authors/{id}/inbox
     '''
     def put(self, request, pk):
        inbox = Inbox.objects.get_or_create(author__id=pk)[0]

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)

        if request.data["type"] == "Follow":
            pass
        if request.data["type"] == "post":
            author = None
            try:
                author = User.objects.get(id=request.data["author"]["id"])
            except:
                response = requests.get(request.data["author"]["global_id"])

                if response.status_code == 200:
                    try:
                        data = response.json()
                        serializer = RemoteUserSerializer(data={"id": data["id"], "global_id": data["global_id"], "url": data["url"], "email": data["email"], "profileImage": data["profileImage"], "profileBackgroundImage": data["profileBackgroundImage"], "github": data["github"], "displayName": data["displayName"]})
                        if serializer.is_valid():
                            author = serializer.save()
                        else: 
                            print(serializer.errors)
                    except Exception as e:
                        print(e)
            
            post_obj = None
            try:
                post_obj = Post.objects.get(id=request.data["post"]["id"])
            except:
                print("DATA:",request.data["post"])
                response = requests.get(request.data["post"]["global_id"])

                if response.status_code == 200:
                    try:
                        data = response.json()
                        serializer = RemotePostSerializer(data={"id": data["id"], "global_id": data["global_id"], "url": data["url"], "host": data["host"], "content": data["content"], "contentType": data["contentType"], "published": data["published"], "visibility": data["visibility"], "origin": data["origin"], "description": data["description"], "author": request.data["author"]["id"]})
                        if serializer.is_valid():
                            post_obj = serializer.save()
                        else: 
                            print(serializer.errors)
                    except Exception as e:
                        print(e)
            
            inbox.post.add(post_obj)
            return Response({"Title":"Done"}, status = status.HTTP_200_OK)
        if request.data["type"] == "comment":
            pass
        if request.data["type"] == "liked":
            pass
        # if response and realAuthor == response[1]["user_id"]:
        #     if serializer.is_valid():
        #         serializer.save(author=author)
        #         return Response(serializer.data, status = status.HTTP_200_OK)
        #     else:
        #         return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST) # Need to change the error message
        # else:
        #     return Response({"title": "Unauthorized", "message": "You are not authorized to update this post"}, status = status.HTTP_401_UNAUTHORIZED)
     '''
     DELETE /authors/{id}/inbox
     '''
     def delete(self, request, pk):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, context={'request': request})
        realAuthor = serializer.get_author(post)["id"]
        if response and realAuthor == response[1]["user_id"]:
            post.delete()
            return Response({"title": "Successfully Deleted", "message": "Post was deleted"}, status = status.HTTP_200_OK)
        return Response({"title": "Unauthorized", "message": "You are not authorized to delete this post"}, status = status.HTTP_401_UNAUTHORIZED)
     