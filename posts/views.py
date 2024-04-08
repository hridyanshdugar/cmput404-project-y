from django.http import JsonResponse
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from backend.permissions import RemoteOrSessionAuthenticated, SessionAuthenticated
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
     permission_classes = [ RemoteOrSessionAuthenticated ]

     '''
     GET /authors/{id}/posts/{id}
     '''
     def get(self, request, author_id, post_id):
        # add logs incrementing number by 1 each time
        print(post_id)
        print(" hi 3")
        user = get_object_or_404(User, id=author_id)
        print(" hi 4")
        if user.host == Node.objects.get(is_self=True).url:
            print(" hi 5")
            post = get_object_or_404(Post, id=post_id)
            print(" hi 6")
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            try:
                print(" hi 7")
                url = user.host + "api/authors/" + str(author_id) + "/posts/" + str(post_id)
                auth = Node.objects.get(url = user.host)
                response = requests.get(url, timeout=20, auth=HTTPBasicAuth(auth.username, auth.password))
                if response.status_code == 200:
                    rbody = response.json()
                    print("Response Body: ", rbody)
                    return Response(data = rbody, status = status.HTTP_200_OK)
                else:
                    print(f"1Request to {user.host} failed with status code: {response.status_code} : {url} : {response.content}")
                print(" hi 8")
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
     def delete(self, request, author_id, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response({"title": "Successfully Deleted", "message": "Post was deleted"}, status = status.HTTP_200_OK)
     
     '''
     PATCH /authors/{id}/posts/{id} and /posts/{id}
     '''
     def patch(self, request, author_id, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostEditSerializer(post, partial=True,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"title": "Successfully Updated", "message": "Post was updated"}, status = status.HTTP_200_OK)
        return Response({"title": "Bad Request", "message": "Invalid Request Sent"}, status = status.HTTP_400_BAD_REQUEST)

class AllPostsView2(APIView):
     permission_classes = [ SessionAuthenticated ]

     pagination = Pager()
     '''
     GET /authors/{id}/posts2/
     '''
     def get(self, request, author_id):
        print("bbbdffffffffffffffffffffffff", author_id)
        author = User.objects.get(id=author_id)
        print("bbbdffffffffffffffffffffffff 2", author)

        friends = []
        for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True),many=True).data:
            for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True),many=True).data:
                if follower["actor"]["id"] == follow["object"]["id"]:
                    friends.append(follower)
        friends = [friend["actor"]["id"].split("/")[-1] for friend in friends]   
        print("bijbbbbbbbbbbbbbbbbbbj34343", friends)    
        posts = Post.objects.filter(Q(author__id=author.id) | Q(visibility="FRIENDS", author__id__in=friends) | Q(visibility="PUBLIC")).order_by('-published') 
        page_number = request.GET.get('page') or 1
        posts = self.pagination.paginate_queryset(posts, request, view=self)
        
        if posts is not None:
            serializer = PostSerializer(posts, many=True, context={'request': request})
            data = serializer.data
            return Response(data, status = status.HTTP_200_OK)
        else:
            return Response("hi", status = status.HTTP_400_BAD_REQUEST)


class AllPostsView(APIView):
     permission_classes = [ RemoteOrSessionAuthenticated ]

     pagination = Pager()
     '''
     GET /authors/{id}/posts/
     '''
     def get(self, request, author_id):
        if User.objects.filter(id=author_id,host=Node.objects.get(is_self=True).url).exists():
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
            nodes = Node.objects.filter(is_self=False)

            for node in nodes:
                print(node.url + "api/authors/" + str(author_id) + "/posts/")
                try:
                    response = requests.get(node.url + "api/authors/" + str(author_id) + "/posts/", timeout=20, auth=HTTPBasicAuth(node.username, node.password))
                    
                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                            print("GOT DATA: ",response_data)
                            return Response(response_data, status = status.HTTP_200_OK)
                        except JSONDecodeError:
                            print(f"Invalid JSON response from {node.url}: {response.text}")
                    else:
                        print(f"2Request to {node.url} failed with status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Request to {node.url} failed: {e}")
            return Response(status=status.HTTP_404_NOT_FOUND)

class PostsView(APIView):
     permission_classes = [ RemoteOrSessionAuthenticated ]
    
     pagination = Pager()
     '''
     GET /authors/{id}/posts/ and /posts/
     '''
     def get(self, request, author_id):
        posts = Post.objects.filter(visibility="PUBLIC", author__id=author_id)
        if User.objects.filter(id=author_id,host=Node.objects.get(is_self=True).url).exists():
            serializer = PostSerializer(posts, many=True, context={'request': request})
            data = dict()
            data["items"] = serializer.data
            data["type"] = "posts"
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
            if request.data.get("title") != "Share":
                serializer.save(author=author)
            valid_post = True
            print("yes1")
            if request.data.get("contentType") == "text/post": #this means the request is a shared post (share button was clicked)
                valid_post = False
            print("Valid Post: ", valid_post, "Request Data: ", request.data)
            if valid_post:
                # loops through followers and sends the post to them
                print("Visibility: ", request.data.get("visibility"))
                print("dsfhsdif", serializer.data)
                if request.data.get("visibility") == "PUBLIC":
                    for i in FollowStatus.objects.filter(obj__id=author_id, complete=True):
                        print("Sending to: ", str(i.actor.host) + "api/authors/" + str(i.actor.id.split("/")[-1]) + "/inbox/")
                        # make request post json data to the inbox of the follower
                        auth = Node.objects.get(url = i.actor.host)
                        requests.post(str(i.actor.host) + "api/authors/" + str(i.actor.id.split("/")[-1]) + "/inbox", data = json.dumps(serializer.data), headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(auth.username, auth.password))

                if request.data.get("visibility") == "FRIENDS":
                    for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True), many=True).data:
                        for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True), many=True).data:
                            if follower["actor"]["id"] == follow["object"]["id"]:
                                print("Sending to2: ", follower["actor"]["host"] + "api/authors/" + str(follower["actor"]["id"].split("/")[-1]) + "/inbox")
                                auth = Node.objects.get(url = follower["actor"]["host"])
                                requests.post(follower["actor"]["host"] + "api/authors/" + str(follower["actor"]["id"].split("/")[-1]) + "/inbox", data = json.dumps(serializer.data), headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(auth.username, auth.password))    
                return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        