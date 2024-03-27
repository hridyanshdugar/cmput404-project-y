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
import copy

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
                response = requests.get(user.host + "api/authors/" + str(author_id) + "/posts/" + str(post_id), timeout=20,auth=HTTPBasicAuth(user_auth, pass_auth))
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
        author = User.objects.get(id=author_id)

        friends = []
        for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True),many=True).data:
            for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True),many=True).data:
                if follower["actor"]["id"] == follow["object"]["id"]:
                    friends.append(follower)
        friends = [friend["actor"]["id"] for friend in friends]        

        posts = Post.objects.filter(Q(author=author) | Q(visibility="FRIENDS", author__id__in=friends) | Q(visibility="PUBLIC")).order_by('-published') 
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
     POST /authors/{id}/posts/
     '''
     def post(self, request, author_id=None):
        author = None
        try:
            author = User.objects.get(id=author_id)
        except User.DoesNotExist:
            return Response({"title": "Author not found.","message": "No valid author for the post was provided"}, status=status.HTTP_404_NOT_FOUND)
    
        bob = copy.deepcopy(request.data)
        bob["author"] = author

        serializer = PostSerializer(data = bob, context={'request': request})
        if serializer.is_valid():
            pppobje = serializer.save(author=author)
            valid_post = True
            print("yes1")
            if request.data.get("contentType") == "text/post": #this means the request is a shared post (share button was clicked)
                print("yes2")
                original_post_id = request.data.get("content")
                print("yes3", original_post_id)
                #replace request.data with content of the actual post but maintain source of shared post
                post_response = requests.get(str(Node.objects.get(is_self=True).url) + "api/posts/" + original_post_id)
                print("yes4")
                print("Post Response: ", post_response.status_code)

                if post_response.status_code == 200:
                    print("yes5")
                    original_post_data = post_response.json()
                    print("Original Post Data: ", original_post_data)
                    bob = copy.deepcopy(original_post_data)
                    print("yes6")
                    serializer = PostSerializer(data = bob, context={'request': post_response})
                    print("yes7")
                else:
                    print("failed")
                    valid_post = False
            print("Valid Post: ", valid_post, "Request Data: ", request.data)
            if valid_post:
                # loops through followers and sends the post to them
                print("Visibility: ", request.data.get("visibility"))
                print("dsfhsdif", serializer.data)
                if request.data.get("visibility") == "PUBLIC":
                    for i in FollowStatus.objects.filter(obj__id=author_id, complete=True):
                        print("Sending to: ", str(i.actor.host) + "api/authors/" + str(i.actor.id) + "/inbox/")
                        # make request post json data to the inbox of the follower
                        requests.post(str(i.actor.host) + "api/authors/" + str(i.actor.id) + "/inbox/", data = json.dumps(serializer.data), headers={'Content-Type': 'application/json'})

                if request.data.get("visibility") == "FRIENDS":
                    for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True)).data:
                        for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True)).data:
                            if follower["actor"]["id"] == follow["object"]["id"]:
                                print("Sending to2: ", follower["object"]["host"] + "api/authors/" + str(follower["object"]["id"]) + "/inbox/")
                                requests.post(follower["object"]["host"] + "api/authors/" + str(follower["object"]["id"]) + "/inbox/", data = json.dumps(serializer.data), headers={'Content-Type': 'application/json'})    
                return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        