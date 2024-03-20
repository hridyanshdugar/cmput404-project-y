from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Inbox, Post
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer, PostEditSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication

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
        inbox = Inbox.objects.get(author=pk)
        try:
            author = User.objects.get(id=request.data.get("author"))
        except User.DoesNotExist:
            return Response({"title": "Author not found.","message": "No valid author for the post was provided"}, status=status.HTTP_404_NOT_FOUND)

        request.data["author"] = post.author

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)

        if request.data["type"] == "Follow":
            pass
        if request.data["type"] == "post":
            serializer = PostSerializer(data = request.data, context={'request': request})
            inbox.objects.add(serializer)
            if serializer.is_valid():
                serializer.save(author=author)
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
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
     