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
        """
        Get the likes on a specific post by a specific user
        """
        user = get_object_or_404(User, id=author_id)
        if user.host == Node.objects.get(is_self=True).url:
            print("hihihi 1", author_id, post_id)
            Likes = PostLike.objects.filter(post__id=post_id)
            print("hihihi 2")
            serializer = PostLikeSerializer(Likes, many=True)
            print("hihihi 3")
            return Response({"type": "liked", "items": serializer.data}, status = status.HTTP_200_OK)
        else:
            try:
                print(" hi 7")
                url = user.host + "api/authors/" + str(author_id) + "/posts/" + str(post_id) + "/likes"
                auth = Node.objects.get(url = user.host)
                response = requests.get(url, timeout=20, auth=HTTPBasicAuth(auth.username, auth.password))
                if response.ok:
                    rbody = response.json()
                    print("3434Response Body: ", rbody, url)
                    return Response(data = rbody, status = status.HTTP_200_OK)
                else:
                    print(f"Requ45est to {user.host} failed with status code: {response.status_code} : {url}")
                print(" hi 8", response.text)
            except requests.exceptions.RequestException as e:
                print(f"Req3est to {user.host} failed: {e}")     
            return Response({"title": "Likes not found.","message": "Likes for the post were not found"}, status=status.HTTP_404_NOT_FOUND)

class PostLikesViewPK(APIView):
     permission_classes = [ RemoteOrSessionAuthenticated ]
     '''
     GET /authors/{id}/posts/{post_id}/likes
     '''
     def get(self, request, author_id, post_id):
        """
        Get the likes on a specific post by a specific user
        """
        print("hihihi 1", author_id, post_id)
        Likes = PostLike.objects.filter(post__id=post_id)
        print("hihihi 2")
        serializer = PostLikeSerializer(Likes, many=True)
        print("hihihi 3")
        return Response({"type": "liked", "items": serializer.data}, status = status.HTTP_200_OK)

     '''
     PUT /authors/{id}/posts/{post_id}/likes
     '''
     def put(self, request, author_id, post_id):
        """
        Send a like to the inbox of a specific user
        """
        body = copy.deepcopy(request.body)
        user = get_object_or_404(User, id=author_id)
        auth = Node.objects.get(url = user.host)
        print("name", user.displayName)
        print("url", str(user.host) + "api/authors/" + author_id + "/inbox")
        res = requests.post(str(user.host) + "api/authors/" + author_id + "/inbox", headers={'Content-Type': 'application/json'},
        data = body, auth=HTTPBasicAuth(auth.username, auth.password))
        print("hihihi 5")
        return Response(res.json(), status = res.status_code)

     
     '''
     DELETE /authors/{id}/posts/{post_id}/likes
     '''
     def delete(self, request, author_id, post_id):
        """
        Unlike a specific post by a specific user
        """
        Like = get_object_or_404(PostLike,author__id=author_id,post__id=post_id)
        Like.delete()
        return Response({"Title": "Successfully Deleted","Message": "Successfully Deleted"}, status = status.HTTP_200_OK)

class PostLikesView(APIView):
     permission_classes = [ RemoteOrSessionAuthenticated ]
     
     def get(self, request, author_id):
        """
        Get all the likes on a post 
        """
        Likes = PostLike.objects.filter(author__id=author_id)
        serializer = PostLikeSerializer(Likes, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
     