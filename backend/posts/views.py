from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Post
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404


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
        serializer = PostSerializer(post, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST) # Need to change the error message
     '''
     DELETE /authors/{id}/posts/{id} and /posts/{id}
     '''
     def delete(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        post.delete()
        return Response({"title": "Successfully Deleted", "message": "Post was deleted"}, status = status.HTTP_200_OK)

class PostsView(APIView):
     pagination = Pager()
     '''
     GET /authors/{id}/posts/ and /posts/
     '''
     def get(self, request):
        posts = Post.objects.filter(visibility="PUBLIC") # No private and unlisted
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
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)