from django.shortcuts import render
import requests
from .serializers import PostLikeSerializer, EditPostLikeSerializer, CommentLikeSerializer, EditCommentLikeSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import PostLike, CommentLike
from posts.models import Post
from comments.models import Comment
from users.models import User
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from nodes.views import is_basicAuth, basicAuth
import copy

class PostLikesViewPK(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')
     
     def get(self, request, author_id, post_id):
        Like = get_object_or_404(PostLike,author__id=author_id,post__id=post_id)
        serializer = PostLikeSerializer(Like)
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     PUT /authors/{id}/posts/ and /posts/
     '''
     def put(self, request, author_id, post_id):
        print(author_id)
        print("dobgg 1")
        user = get_object_or_404(User,id=author_id)
        print("dobgg2")

        post = get_object_or_404(Post,id=post_id)
        print("dobgg 3")
        body = copy.deepcopy(request.body)
        print("dobgg 3", str(request.data["author"]["host"]) + "api/authors/" + str(request.data["author"]["id"]) + "/inbox/", body)

        requests.post(str(request.data["author"]["host"]) + "api/authors/" + str(request.data["author"]["id"]) + "/inbox/", data = body)
        print("dobgg 4")

        request.data['post'] = post_id
        print("dobgg 5")

        serializer = EditPostLikeSerializer(data=request.data)
        if serializer.is_valid():
            Like = serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            print(serializer.errors)
        return Response({"Title": "Unsuccessfully Added","Message": "Unsuccessfully Added"}, status = status.HTTP_400_BAD_REQUEST)
     
     '''
     DELETE /authors/{id}/posts/ and /posts/
     '''
     def delete(self, request, author_id, post_id):
        Like = get_object_or_404(PostLike,author__id=author_id,post__id=post_id)
        Like.delete()
        return Response({"Title": "Successfully Deleted","Message": "Successfully Deleted"}, status = status.HTTP_200_OK)

class PostLikesView(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')
     
     def get(self, request, author_id):
        Likes = PostLike.objects.filter(author__id=author_id)
        serializer = PostLikeSerializer(Likes, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)




class CommentLikesViewPK(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')
     
     def get(self, request, author_id, comment_id):
        Like = get_object_or_404(CommentLike,author__id=author_id,comment__id=comment_id)
        serializer = CommentLikeSerializer(Like)
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     PUT /authors/{id}/posts/ and /posts/
     '''
     def put(self, request, author_id, comment_id):
        print(author_id)
        usr = get_object_or_404(User,id=author_id)
        post = get_object_or_404(Comment,id=comment_id)
        print("NO")

        new_data = request.data.copy()
        new_data['author'] = author_id
        new_data['comment'] = comment_id

        serializer = EditCommentLikeSerializer(data=new_data)
        if serializer.is_valid():
            Like = serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"Title": "Unsuccessfully Added","Message": "Unsuccessfully Added"}, status = status.HTTP_400_BAD_REQUEST)
     
     '''
     DELETE /authors/{id}/posts/ and /posts/
     '''
     def delete(self, request, author_id, post_id):
        Like = get_object_or_404(CommentLike,author__id=author_id,post__id=post_id)
        Like.delete()
        return Response({"Title": "Successfully Deleted","Message": "Successfully Deleted"}, status = status.HTTP_200_OK)

class CommentLikesView(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')
     
     def get(self, request, author_id):
        Likes = CommentLike.objects.filter(author__id=author_id)
        serializer = CommentLikeSerializer(Likes, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
