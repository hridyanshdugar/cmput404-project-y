from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Comment
from rest_framework.pagination import PageNumberPagination
from .serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from posts.models import Post
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from followers.views import getFriends
import json
from nodes.views import is_basicAuth, basicAuth

class Pager(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

class CommentsViewPK(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')

     '''
     GET /authors/{id}/posts/{id}/comments/{id} and posts/{id}/comments/{id}
     '''
     def get(self, request, fk, pk):
        print(pk)
        
        comment = get_object_or_404(Comment, id=pk)
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        requestAuthor = User.objects.get(id=response[1]["user_id"])

        if comment.post.visibility == "FRIENDS" and str(requestAuthor.id) != str(comment.post.author.id):
            friends = json.loads(getFriends(request, str(comment.post.author.id)).content) # request is useless
            for friend in friends:
                if str(friend) == str(requestAuthor.id):
                    serializer = CommentSerializer(comment, context={'request': request})
                    return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"title": "Unauthorized", "message": "You are not authorized to view this comment"}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     PUT /authors/{id}/posts/{id}/comments/{id} and posts/{id}/comments/{id}
     '''
     def put(self, request, fk, pk):
        comment = get_object_or_404(Comment, id=pk)

        try:
            post = Post.objects.get(id=fk)
        except Post.DoesNotExist:
            return Response({"title": "Post not found", "message": "No valid post for the comment was provided" })
        
        if request.data.get("author"):
            author = None
            try:
                author = User.objects.get(id=request.data.get(author))
            except User.DoesNotExist:
                return Response({"title": "Author not found.","message": "No valid author for the comment was provided"}, status=status.HTTP_404_NOT_FOUND)

        request.data["author"] = comment.author

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        serializer = CommentSerializer(comment, data = request.data, partial=True, context={'request': request})
        realAuthor = serializer.get_author(comment)["id"]

        if response and realAuthor == response[1]["user_id"]:
            if serializer.is_valid():
                serializer.save(author=author)
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST) # Need to change the error message
        else:
            return Response({"title": "Unauthorized", "message": "You are not authorized to update this comment"}, status = status.HTTP_401_UNAUTHORIZED)
     '''
     DELETE /authors/{id}/posts/{id}/comments/{id} and posts/{id}/comments/{id}
     '''
     def delete(self, request, fk, pk):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(comment, context={'request': request})
        realAuthor = serializer.get_author(comment)["id"]
        if response and realAuthor == response[1]["user_id"]:
            comment.delete()
            return Response({"title": "Successfully Deleted", "message": "Comment was deleted"}, status = status.HTTP_200_OK)
        return Response({"title": "Unauthorized", "message": "You are not authorized to delete this comment"}, status = status.HTTP_401_UNAUTHORIZED)

class CommentsView(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')
    
     pagination = Pager()
     '''
     GET /authors/{id}/posts/{id}/comments/ and posts/{id}/comments/
     '''
     def get(self, request, fk):
        comments=None

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        author = User.objects.get(id=response[1]["user_id"])

        friends = json.loads(getFriends(request, author.id).content)

        if request.GET.get('local',False):
            comments = Comment.objects.filter(Q(host=request.GET.get('host'), post=fk))
            # comments = Comment.objects.filter(Q(visibility="PUBLIC", host=request.GET.get('host')) | Q(visibility="FRIENDS")) # FINISH UP
        else:
            comments = Comment.objects.filter(Q(post=fk, post__visibility__in=["PUBLIC", "UNLISTED"]) | Q(post=fk, post__visibility="FRIENDS", author__id__in=friends) | Q(post=fk, post__author=author.id)).order_by('-published')
        page_number = request.GET.get('page') or 1
        page = self.pagination.paginate_queryset(comments, request, view=self)
        if page is not None:
            serializer = CommentSerializer(page, many=True, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

     '''
     POST /authors/{id}/posts/{id}/comments/ and posts/{id}/comments/
     '''
     def post(self, request, fk):
        author = None

        try:
            post = Post.objects.get(id=fk)
        except Post.DoesNotExist:
            return Response({"title": "Post not found", "message": "No valid post for the comment was provided" })
        
        try:
            author = User.objects.get(id=request.data.get("author"))
        except User.DoesNotExist:
            return Response({"title": "Author not found.","message": "No valid author for the comment was provided"}, status=status.HTTP_404_NOT_FOUND)
        
        request.data["author"] = author

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        serializer = CommentSerializer(data = request.data, context={'request': request})

        if response and str(author.id) == response[1]["user_id"]:
            if serializer.is_valid():
                serializer.save(author=author)
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"title": "Unauthorized", "message": "You are not authorized to create this comment"}, status = status.HTTP_401_UNAUTHORIZED)