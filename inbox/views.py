from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Inbox, Post
from comments.models import Comment
from rest_framework.pagination import PageNumberPagination
from posts.serializers import PostSerializer
from likes.serializers import EditCommentLikeSerializer, EditPostLikeSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import RemoteUserSerializer
from posts.serializers import RemotePostSerializer
from .serializers import InboxSerializer
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
        post = get_object_or_404(Inbox, author__id=pk)
        print("GOT")
        serializer = InboxSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     PUT /authors/{id}/inbox
     '''
     def put(self, request, pk):
        inbox = Inbox.objects.get_or_create(id=pk)[0]

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
            inbox.author = author
            inbox.save()
            return Response({"Title":"Done"}, status = status.HTTP_200_OK)
        if request.data["type"] == "comment":
            pass
        if request.data["type"] == "liked":
            if "comment" in request.data["object"]: 
                usr = get_object_or_404(User,id=request.data["id"])
                post = get_object_or_404(Comment,id=request.data["object"].split("/")[-1])
                print("NO")

                new_data = request.data.copy()
                new_data['author'] = request.data["id"]
                new_data['comment'] = request.data["object"].split("/")[-1]

                serializer = EditCommentLikeSerializer(data=new_data)
                if serializer.is_valid():
                    Like = serializer.save()
                    inbox.commentLikes.add(Like)
                    inbox.author = usr
                    inbox.save()  
                    return Response(serializer.data, status = status.HTTP_200_OK)
                return Response({"Title": "Unsuccessfully Added","Message": "Unsuccessfully Added"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                usr = get_object_or_404(User,id=request.data["id"])
                post = get_object_or_404(Post,id=request.data["object"].split("/")[-1])
                print("NO")

                new_data = request.data.copy()
                new_data['author'] = request.data["id"]
                new_data['post'] = request.data["object"].split("/")[-1]

                serializer = EditPostLikeSerializer(data=new_data)

                if serializer.is_valid():
                    Like = serializer.save()
                    inbox.postLikes.add(Like)
                    inbox.author = usr
                    inbox.save()                    
                    return Response({"Title":"Done"}, status = status.HTTP_200_OK)
                else:
                    print(serializer.errors)
                return Response({"Title": "Unsuccessfully Added","Message": "Unsuccessfully Added"}, status = status.HTTP_400_BAD_REQUEST)
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
     