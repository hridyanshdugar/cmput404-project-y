from django.shortcuts import render
import requests

from backend.permissions import RemoteOrSessionAuthenticated, SessionAuthenticated
from nodes.models import Node
from .serializers import PostLikeSerializer, EditPostLikeSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import PostLike
from posts.models import Post
from comments.models import Comment
from users.models import User
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from nodes.views import is_basicAuth, basicAuth
from requests.auth import HTTPBasicAuth
import copy

class PostLikesViewPK2(APIView):
     permission_classes = [ SessionAuthenticated ]
     
     def get(self, request, author_id, post_id):
        user = get_object_or_404(User, id=author_id)
        if user.host == Node.objects.get(is_self=True).url:
            print("hihihi 1", author_id, post_id)
            Likes = PostLike.objects.filter(author__id=author_id,post__id=post_id)
            print("hihihi 2")
            serializer = PostLikeSerializer(Likes, many=True)
            print("hihihi 3")
            return Response({"type": "Liked", "items": serializer.data}, status = status.HTTP_200_OK)
        else:
            try:
                print(" hi 7")
                url = user.host + "api/authors/" + str(author_id) + "/posts/" + str(post_id) + "/likes"
                auth = Node.objects.get(url = user.host)
                response = requests.get(url, timeout=20, auth=HTTPBasicAuth(auth.username, auth.password))
                if response.status_code == 200:
                    rbody = response.json()
                    print("Response Body: ", rbody)
                    return Response(data = rbody, status = status.HTTP_200_OK)
                else:
                    print(f"Request to {user.host} failed with status code: {response.status_code} : {url}")
                print(" hi 8")
            except requests.exceptions.RequestException as e:
                print(f"Request to {user.host} failed: {e}")     

class PostLikesViewPK(APIView):
     permission_classes = [ RemoteOrSessionAuthenticated ]
     
     def get(self, request, author_id, post_id):
        print("hihihi 1", author_id, post_id)
        Likes = PostLike.objects.filter(author__id=author_id,post__id=post_id)
        print("hihihi 2")
        serializer = PostLikeSerializer(Likes, many=True)
        print("hihihi 3")
        return Response({"type": "Liked", "items": serializer.data}, status = status.HTTP_200_OK)

     '''
     PUT /authors/{id}/posts/ and /posts/
     '''
     def put(self, request, author_id, post_id):
        body = copy.deepcopy(request.body)
        auth = Node.objects.get(url = request.data["author"]["host"])
        res = requests.post(str(request.data["author"]["host"]) + "api/authors/" + author_id + "/inbox", data = body, auth=HTTPBasicAuth(auth.username, auth.password))
        print("hihihi 5")
        return Response(res.json(), status = status.HTTP_200_OK)

     
     '''
     DELETE /authors/{id}/posts/ and /posts/
     '''
     def delete(self, request, author_id, post_id):
        Like = get_object_or_404(PostLike,author__id=author_id,post__id=post_id)
        Like.delete()
        return Response({"Title": "Successfully Deleted","Message": "Successfully Deleted"}, status = status.HTTP_200_OK)

class PostLikesView(APIView):
     permission_classes = [ RemoteOrSessionAuthenticated ]
     
     def get(self, request, author_id):
        Likes = PostLike.objects.filter(author__id=author_id)
        serializer = PostLikeSerializer(Likes, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
     