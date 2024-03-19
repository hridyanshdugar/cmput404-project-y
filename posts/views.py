from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Post
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer, PostEditSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication


class Pager(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

class PostsViewPK(APIView):

     '''
     GET /authors/{id}/posts/{id} and /posts/{id}
     '''
     def get(self, request, pk):
        print(pk)
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

     '''
     PUT /authors/{id}/posts/{id} and /posts/{id}
     '''
     def put(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        try:
            author = User.objects.get(id=request.data.get("author"))
        except User.DoesNotExist:
            return Response({"title": "Author not found.","message": "No valid author for the post was provided"}, status=status.HTTP_404_NOT_FOUND)

        request.data["author"] = post.author

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        serializer = PostSerializer(post, data = request.data, partial=True, context={'request': request})
        realAuthor = serializer.get_author(post)["id"]

        if response and realAuthor == response[1]["user_id"]:
            if serializer.is_valid():
                serializer.save(author=author)
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST) # Need to change the error message
        else:
            return Response({"title": "Unauthorized", "message": "You are not authorized to update this post"}, status = status.HTTP_401_UNAUTHORIZED)
     '''
     DELETE /authors/{id}/posts/{id} and /posts/{id}
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
     
     '''
     PATCH /authors/{id}/posts/{id} and /posts/{id}
     '''
     def patch(self, request, pk):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        post = get_object_or_404(Post, id=pk)
        serializer = PostEditSerializer(post, partial=True,data = request.data)
        
        if response and serializer.is_valid():
            serializer.save()
            return Response({"title": "Successfully Updated", "message": "Post was updated"}, status = status.HTTP_200_OK)
        return Response({"title": "Bad Request", "message": "Invalid Request Sent"}, status = status.HTTP_400_BAD_REQUEST)

class PostsView(APIView):
     pagination = Pager()
     '''
     GET /authors/{id}/posts/ and /posts/
     '''
     def get(self, request):
        posts=None
        if request.GET.get('local',False):
            posts = Post.objects.filter(Q(visibility="PUBLIC", host=request.GET.get('host')) | Q(visibility="FRIENDS")) # FINISH UP
        else:
            posts = Post.objects.filter(visibility="PUBLIC").order_by('-published') # No private and unlisted
        page_number = request.GET.get('page') or 1
        page = self.pagination.paginate_queryset(posts, request, view=self)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

     '''
     POST /authors/{id}/posts/ and /posts/
     '''
     def post(self, request):
        author = None
        try:
            author = User.objects.get(id=request.data.get("author"))
        except User.DoesNotExist:
            return Response({"title": "Author not found.","message": "No valid author for the post was provided"}, status=status.HTTP_404_NOT_FOUND)

        request.data["author"] = author

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        serializer = PostSerializer(data = request.data, context={'request': request})
        if response and str(author.id) == response[1]["user_id"]:
            if serializer.is_valid():
                serializer.save(author=author)
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"title": "Unauthorized", "message": "You are not authorized to create this post"}, status = status.HTTP_401_UNAUTHORIZED)