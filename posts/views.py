from django.http import JsonResponse
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Post
from nodes.models import Node
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer, PostEditSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from followers.views import getFriends, FollowStatus
import json
from requests.exceptions import JSONDecodeError
from nodes.views import is_basicAuth, basicAuth
from requests.auth import HTTPBasicAuth
from rest_framework.response import Response
from followers.serializers import FollowSerializer


class Pager(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

class PostsViewPK(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')

     '''
     GET /authors/{id}/posts/{id}
     '''
     def get(self, request, author_id, post_id):
        user_auth = get_object_or_404(Node,is_self=True).username
        pass_auth = get_object_or_404(Node,is_self=True).password
        print(post_id)
        
        user = get_object_or_404(User, id=author_id)
        if user.host == Node.objects.get(is_self=True).url:
            post = get_object_or_404(Post, id=post_id)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            try:
                response = requests.get(user.host + "api/authors/" + str(author_id) + "/posts/" + str(post_id) + "/", timeout=20,auth=HTTPBasicAuth(user_auth, pass_auth))
                if response.status_code == 200:
                    return Response(response.body, status = status.HTTP_200_OK)
                else:
                    print(f"Request to {user.host} failed with status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request to {user.host} failed: {e}")

     '''
     PUT /authors/{id}/posts/{id} and /posts/{id}
     '''
     def put(self, request, author_id, post_id):
        post = get_object_or_404(Post, id=post_id)
        try:
            author = User.objects.get(id=request.data.get("author"))
        except User.DoesNotExist:
            return Response({"title": "Author not found.","message": "No valid author for the post was provided"}, status=status.HTTP_404_NOT_FOUND)


        request.data["author"] = post.author

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        serializer = PostSerializer(post, data = request.data, partial=True, context={'request': request})
        realAuthor = serializer.get_author(post)["id"]

        if response and (realAuthor == response[1]["user_id"] or author_id == realAuthor):
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
        post = get_object_or_404(Post, id=pk)
        post.delete()
        return Response({"title": "Successfully Deleted", "message": "Post was deleted"}, status = status.HTTP_200_OK)
     
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

class AllPostsView2(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')

     pagination = Pager()
     '''
     GET /authors/{id}/posts2/
     '''
     def get(self, request, author_id):
        if User.objects.filter(id=author_id,host=Node.objects.get(is_self=True).url).exists():
            JWT_authenticator = JWTAuthentication()
            response = JWT_authenticator.authenticate(request)
            author = User.objects.get(id=author_id)
            friends = json.loads(getFriends(author_id))
            posts = Post.objects.filter(Q(author=author_id) | Q(visibility="FRIENDS", author__id__in=friends) | Q(visibility="PUBLIC")).order_by('-published') 
            page_number = request.GET.get('page') or 1
            posts = self.pagination.paginate_queryset(posts, request, view=self)
            if posts is not None:
                serializer = PostSerializer(posts, many=True, context={'request': request})
                data = serializer.data
                return Response(data, status = status.HTTP_200_OK)
            else:
                return Response("hi", status = status.HTTP_400_BAD_REQUEST)


class AllPostsView(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')

     pagination = Pager()
     '''
     GET /authors/{id}/posts/
     '''
     def get(self, request, author_id):
        if User.objects.filter(id=author_id,host=Node.objects.get(is_self=True).url).exists():
            JWT_authenticator = JWTAuthentication()
            response = JWT_authenticator.authenticate(request)
            author = User.objects.get(id=author_id)
            posts = Post.objects.filter(Q(visibility="PUBLIC", author=author_id)).order_by('-published') 
            page_number = request.GET.get('page') or 1
            posts = self.pagination.paginate_queryset(posts, request, view=self)
            if posts is not None:
                serializer = PostSerializer(posts, many=True, context={'request': request})
                data = serializer.data
                return Response(data, status = status.HTTP_200_OK)
            else:
                return Response("hi", status = status.HTTP_400_BAD_REQUEST)
        else:
            user_auth = get_object_or_404(Node,is_self=True).username
            pass_auth = get_object_or_404(Node,is_self=True).password
            nodes = Node.objects.filter(is_self=False)

            for node in nodes:
                print(node.url + "api/authors/" + str(author_id) + "/posts/")
                try:
                    response = requests.get(node.url + "api/authors/" + str(author_id) + "/posts/", timeout=20,auth=HTTPBasicAuth(user_auth, pass_auth))
                    
                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                            print("GOT DATA: ",response_data)
                            return Response(response_data, status = status.HTTP_200_OK)
                        except JSONDecodeError:
                            print(f"Invalid JSON response from {node.url}: {response.text}")
                    else:
                        print(f"Request to {node.url} failed with status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Request to {node.url} failed: {e}")
            return Response(status=status.HTTP_404_NOT_FOUND)

class PostsView(APIView):
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')
    
     pagination = Pager()
     '''
     GET /authors/{id}/posts/ and /posts/
     '''
     def get(self, request, author_id):
        posts = Post.objects.filter(visibility="PUBLIC", author__id=author_id)
        if User.objects.filter(id=author_id,host=Node.objects.get(is_self=True).url).exists():
            serializer = PostSerializer(posts, many=True, context={'request': request})
            data = serializer.data
            return Response(data, status = status.HTTP_200_OK)
        else:
            return Response("BAD", status = status.HTTP_400_BAD_REQUEST)

     '''
     POST /authors/{id}/posts/ and /posts/
     '''
     def post(self, request, author_id):
        author = None
        try:
            author = User.objects.get(id=author_id)
        except User.DoesNotExist:
            return Response({"title": "Author not found.","message": "No valid author for the post was provided"}, status=status.HTTP_404_NOT_FOUND)

        request.data["author"] = author

        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        serializer = PostSerializer(data = request.data, context={'request': request})
        print(response)
        if serializer.is_valid():
            serializer.save(author=author)
            valid_post = True
            
            if request.data.get("contentType") == "text/post": #this means the request is a shared post (share button was clicked)
                original_post_id = request.data.get("content")
               #replace request.data with content of the actual post but maintain source of shared post
                post_response = requests.get(i.follower.host + "api/posts/" + original_post_id)
                if post_response.status_code == 200:
                    original_post_data = post_response.json()
                    shared_post_source = request.data.get("url")
                    request.data = original_post_data
                    request.data["url"] = shared_post_source
                else:
                    valid_post = False
            
            if valid_post:
                # loops through followers and sends the post to them
                if request.data.get("visibility") == "PUBLIC":
                    for i in FollowStatus.objects.filter(actor=author, complete=True):
                        requests.post(str(i.obj.host) + "api/author/" + str(i.obj.id) + "/inbox/", data = serializer.data)

                if request.data.get("visibility") == "FRIENDS":
                    for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True)).data:
                        for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True)).data:
                            if follower["actor"]["id"] == follow["object"]["id"]:
                                requests.post(follow["object"]["host"] + "api/author/" + str(follow["object"]["id"]) + "/inbox/", data = serializer.data)    
                return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        