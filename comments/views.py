import copy
from urllib.request import HTTPBasicAuthHandler
import uuid
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from requests.auth import HTTPBasicAuth

from backend.permissions import RemoteOrSessionAuthenticated, SessionAuthenticated
from nodes.models import Node
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
from followers.serializers import FollowSerializer
from followers.models import FollowStatus
import requests

class Pager(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

class CommentsViewPK(APIView):
     permission_classes = [ RemoteOrSessionAuthenticated ]

     '''
     GET /authors/{id}/posts/{id}/comments/{id}
     '''
     def get(self, request, author_id, fk, pk):
        """
        Get a specific comment on a specific post by a specific user
        """
        comment = get_object_or_404(Comment, id=pk)
        requestAuthor = User.objects.get(id=author_id)

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
     PUT /authors/{id}/posts/{id}/comments/{id}
     '''
     def put(self, request, author_id, fk, pk):
        """
        Post a comment on a specific post by a specific user
        """
        comment = get_object_or_404(Comment, id=pk)
        requestAuthor = User.objects.get(id=author_id)
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
     DELETE /authors/{id}/posts/{id}/comments/{id}
     '''
     def delete(self, request, author_id, fk, pk):
        """
        Delete a specific comment by a specific user on a specific post
        """
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(comment, context={'request': request})
        realAuthor = serializer.get_author(comment)["id"]
        if response and realAuthor == response[1]["user_id"]:
            comment.delete()
            return Response({"title": "Successfully Deleted", "message": "Comment was deleted"}, status = status.HTTP_200_OK)
        return Response({"title": "Unauthorized", "message": "You are not authorized to delete this comment"}, status = status.HTTP_401_UNAUTHORIZED)

class CommentsView2(APIView):
     permission_classes = [ SessionAuthenticated ]
    
     pagination = Pager()
     '''
     GET /authors/{id}/posts/{id}/comments/ 
     '''
     def get(self, request, author_id, fk):
        """
        Get a specific comment on a specific post by a specific user
        """
        user = get_object_or_404(User, id=author_id)
        if user.host == Node.objects.get(is_self=True).url:
            comments=None

            friends = []
            for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True),many=True).data:
                for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True),many=True).data:
                    if follower["actor"]["id"] == follow["object"]["id"]:
                        friends.append(follower)
            friends = [friend["actor"]["id"].split("/")[-1] for friend in friends]

            if request.GET.get('local',False):
                comments = Comment.objects.filter(Q(host=request.GET.get('host'), post=fk))
                # comments = Comment.objects.filter(Q(visibility="PUBLIC", host=request.GET.get('host')) | Q(visibility="FRIENDS")) # FINISH UP
            else:
                comments = Comment.objects.filter(Q(post=fk, post__visibility__in=["PUBLIC", "UNLISTED"]) | Q(post=fk, post__visibility="FRIENDS", author__id__in=friends) | Q(post=fk, post__author=author_id)).order_by('-published')
            page_number = request.GET.get('page') or 1
            page = self.pagination.paginate_queryset(comments, request, view=self)
            if page is not None:
                serializer = CommentSerializer(page, many=True, context={'request': request})
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
        else:
            try:
                print(" hi 7")

                url = user.host + "api/authors/" + str(author_id) + "/posts/" + str(fk) + "/comments?page=1&size=100"
                auth = Node.objects.get(url = user.host)
                if "web-wizard" in user.host:
                    url = user.host + "api/authors/" + str(author_id) + "/posts/" + str(fk) + "/comments"
                    response = requests.get(url, timeout=20)
                else:
                    response = requests.get(url, timeout=20, auth=HTTPBasicAuth(auth.username, auth.password))
                if response.ok:
                    rbody = response.json()
                    print("big builder 321", rbody)
                    if "comments" in rbody:
                        rbody = rbody["comments"]
                    if "items" in rbody:
                        rbody = rbody["items"]                        
                    print("Response Body: ", rbody)
                    return Response(data = rbody, status = status.HTTP_200_OK)
                else:
                    print(f"Request to {user.host} failed with status code: {response.status_code} : {url}")
                    return Response(data = response.json(), status = response.status_code)
                print(" hi 8")
            except requests.exceptions.RequestException as e:
                print(f"Request to {user.host} failed: {e}")     
                return Response(data = response.json(), status = response.status_code)

class CommentsView(APIView):
     permission_classes = [ RemoteOrSessionAuthenticated ]
    
     pagination = Pager()
     '''
     GET /authors/{id}/posts/{id}/comments/ 
     '''
     def get(self, request, author_id, fk):
        """
        get all the comments on a specific post by a specific user
        """
        comments=None

        friends = []
        for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True),many=True).data:
            for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True),many=True).data:
                if follower["actor"]["id"] == follow["object"]["id"]:
                    friends.append(follower)
        friends = [friend["actor"]["id"].split("/")[-1] for friend in friends]

        if request.GET.get('local',False):
            comments = Comment.objects.filter(Q(host=request.GET.get('host'), post=fk))
            # comments = Comment.objects.filter(Q(visibility="PUBLIC", host=request.GET.get('host')) | Q(visibility="FRIENDS")) # FINISH UP
        else:
            comments = Comment.objects.filter(Q(post=fk, post__visibility__in=["PUBLIC", "UNLISTED"]) | Q(post=fk, post__visibility="FRIENDS", author__id__in=friends) | Q(post=fk, post__author=author_id)).order_by('-published')
        page_number = request.GET.get('page') or 1
        page = self.pagination.paginate_queryset(comments, request, view=self)
        if page is not None:
            serializer = CommentSerializer(page, many=True, context={'request': request})
            data = dict()
            data["comments"] = serializer.data
            data["type"] = "comments"
            return Response(data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

     '''
     POST /authors/{id}/posts/{id}/comments/
     '''
     def post(self, request, author_id, fk):
        """
        Add a comment to a specific post by a specific user
        """
        user = User.objects.get(id=author_id)
        auth = Node.objects.get(url = user.host)
        response = copy.deepcopy(request.data)
        print("burger222", user.host)
        if "depresso" in user.host:
            response['id'] = response['id'] + "/comments/" + str(uuid.uuid4())
        print("buhdafugbhfduiui33483883", response)
        res = requests.post(str(user.host) + "api/authors/" + author_id + "/inbox", headers={'Content-Type': 'application/json'},  data = json.dumps(response), auth=HTTPBasicAuth(auth.username, auth.password))
        return Response(res, status = res.status_code)