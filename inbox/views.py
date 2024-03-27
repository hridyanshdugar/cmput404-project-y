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
from nodes.models import Node
from nodes.views import is_basicAuth, basicAuth
from requests.auth import HTTPBasicAuth
from followers.serializers import FollowSerializer, SaveFollowSerializer
from followers.models import FollowStatus
import json
import copy 
from users.views import download_profile, download_profileBack
class Pager(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

# Create your views here.
class InboxView(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')

     pagination = Pager()

     '''
     GET /authors/{id}/inbox
     '''
     def get(self, request, pk):
        print(pk)
        hi_user = User.objects.get(id=pk)
        post = Inbox.objects.get_or_create(author=hi_user)[0]
        print("GOT")
        serializer = InboxSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     POST /authors/{id}/inbox
     '''
     def post(self, request, pk):
        def get_foreign_user(data):
            response_data = copy.deepcopy(data)["actor"]
            try:
                obj_user = User.objects.get(id=data["actor"]["id"])
            except:
                hasPfp = False
                hasPfpBack = False
                if "profileImage" in response_data:
                    hasPfp = response_data.pop("profileImage")
                if "profileBackgroundImage" in response_data:
                    hasPfpBack = response_data.pop("profileBackgroundImage")
                print(response_data)
                user = None
                serializer = None
                try:
                    user = User.objects.get(id=pk)
                    serializer = RemoteUserSerializer(user,data=response_data,partial=True)
                except Exception as e:
                    print(e)  

                    serializer = RemoteUserSerializer(data=response_data)
                if serializer.is_valid():
                    user = serializer.save()
                    if hasPfp:
                        download_profile(user, hasPfp)
                        response_data['profileImage'] = hasPfp
                    if hasPfpBack:
                        download_profileBack(user, hasPfpBack)
                        response_data['profileBackgroundImage'] = hasPfpBack
                else:
                    print(f"Invalid data from : {serializer.errors}")

        hi_user = User.objects.get(id=pk)
        inbox = Inbox.objects.get_or_create(author=hi_user)[0]

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        print("RESPONSEfdsfdsfsd", request.body)
        data = json.loads(request.body)
        print("big bug", data)
        if data["type"] == "Follow":
            get_foreign_user(data)
        
            
            serializer = SaveFollowSerializer(data={"actor": data["actor"]["id"],"obj":data["object"]["id"], "complete": False})
            if serializer.is_valid():
                if not FollowStatus.objects.filter(actor=data["actor"]["id"],obj=data["object"]["id"]).exists():
                    follow_obj = serializer.save()
                    inbox.author = User.objects.get(id=pk)
                    inbox.followRequest.add(follow_obj)
                    inbox.save()

            return Response({"Title":"Done"}, status = status.HTTP_200_OK)
        if data["type"] == "Unfollow":
            get_foreign_user(data)
            
            req = get_object_or_404(FollowStatus,actor=data["actor"]["id"],obj=data["object"]["id"])
            req.delete()

            return Response({"Title":"Done"}, status = status.HTTP_200_OK)
        if data["type"] == "FollowResponse":
            get_foreign_user(data)
            if data["accepted"]:
                req = get_object_or_404(FollowStatus,actor=data["actor"]["id"],obj=data["object"]["id"])
                req.complete = True
                req.save()
            else:
                req = get_object_or_404(FollowStatus,actor=data["actor"]["id"],obj=data["object"]["id"])
                req.delete()


            return Response({"Title":"Done"}, status = status.HTTP_200_OK)        
        if data["type"] == "post":
            author = None
            print("abc : 1")
            try:
                author = User.objects.get(id=data["author"]["id"])
            except:
                user_auth = get_object_or_404(Node,is_self=True).username
                pass_auth = get_object_or_404(Node,is_self=True).password
                response = requests.get(str(data["author"]["host"]) + "api/authors" + str(data["author"]["id"]) + "/", auth=HTTPBasicAuth(user_auth, pass_auth))

                if response.status_code == 200:
                    try:
                        bob = response.json()
                        serializer = RemoteUserSerializer(data={"id": bob["id"], "url": bob["url"], "displayName": bob["displayName"], "profileImage": bob["profileImage"], "profileBackgroundImage": bob["profileBackgroundImage"], "github": bob["github"], "displayName": bob["displayName"]})
                        if serializer.is_valid():
                            author = serializer.save()
                        else: 
                            print(serializer.errors)
                    except Exception as e:
                        print(e)
            print("abc : 2")
            post_obj = None
            print("abc : 3")
            try:
                print("abc : 4")
                post_obj = Post.objects.get(id=data["id"])
            except:
                print("DATA:",data)
                print("abc : 4")
                user_auth = get_object_or_404(Node,is_self=True).username
                pass_auth = get_object_or_404(Node,is_self=True).password
                response = requests.get(str(data["author"]["host"]) + "api/authors/" + data["author"]["id"] + "/posts/" + str(data["id"]), auth=HTTPBasicAuth(user_auth, pass_auth))
                print("abc : 5")
                if response.status_code == 200:
                    print("abc : 6")
                    try:
                        bob = response.json()
                        print("abc : 7")
                        serializer = RemotePostSerializer(data={"id": bob["id"], "url": bob["url"], "host": bob["host"], "content": bob["content"], "contentType": bob["contentType"], "published": data["published"], "visibility": data["visibility"], "origin": data["origin"], "description": bob["description"], "author": bob["author"]["id"]})
                        print("abc : 8")
                        if serializer.is_valid():
                            print("abc : 9")
                            post_obj = serializer.save()
                            print("abc : 10")
                        else: 
                            print("abc : 11")
                            print(serializer.errors)
                    except Exception as e:
                        print("dfsjafiusdarf78", e)
            print("abc : 12")
            inbox.post.add(post_obj)
            print("abc : 13")
            inbox.author = author
            print("abc : 14")
            inbox.save()
            print("abc : 15")
            return Response({"Title":"Done"}, status = status.HTTP_200_OK)
        if data["type"] == "comment":
            pass
        if data["type"] == "liked":
            if "comment" in data["object"]: 
                user = get_object_or_404(User,id=data["id"])
                post = get_object_or_404(Comment,id=data["object"].split("/")[-1])
                print("NO")

                new_data = data.copy()
                new_data['author'] = data["id"]
                new_data['comment'] = data["object"].split("/")[-1]

                serializer = EditCommentLikeSerializer(data=new_data)
                if serializer.is_valid():
                    Like = serializer.save()
                    inbox.commentLikes.add(Like)
                    inbox.author = user
                    inbox.save()  
                    return Response(serializer.data, status = status.HTTP_200_OK)
                return Response({"Title": "Unsuccessfully Added","Message": "Unsuccessfully Added"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                user = get_object_or_404(User,id=data["id"])
                post = get_object_or_404(Post,id=data["object"].split("/")[-1])
                print("NO")

                new_data = data.copy()
                new_data['author'] = data["id"]
                new_data['post'] = data["object"].split("/")[-1]

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
     