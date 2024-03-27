from json import JSONDecodeError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from users.models import User
from rest_framework.views import APIView
from urllib.parse import unquote
import requests
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from nodes.models import Node
from nodes.views import is_basicAuth, basicAuth
from requests.auth import HTTPBasicAuth
from rest_framework.response import Response
from rest_framework import status
from .serializers import FollowSerializer, SaveFollowSerializer
from .models import FollowStatus
from inbox.models import Inbox
import json
val = URLValidator()
from users.serializers import AuthorSerializer
from users.models import User

def getFollowers(request, author_id=None):
    # user = list(User.objects.filter(id=author_id).values())[0]
    if User.objects.filter(id=author_id).exists():
        user = User.objects.get(id=author_id)
        if user.host == Node.objects.get(is_self=True).url:

            try:
                print("here")
                followers = FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True),many=True).data
            except:
                followers = []
            try:
                following = FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True),many=True).data
            except:
                following = []
            print(followers, following, "AAd")
            friends = []
            for follower in followers:
                for follow in following:
                    if follower["object"]["id"] == follow["actor"]["id"]:
                        friends.append(follower["actor"])

            followers = [follower["actor"] for follower in followers]
            following = [following["object"] for following in following]
            
            print("massive", {
                "type": "followers",
                "items": followers,
                "following": following,
                "friends": friends
            })
            
            return JsonResponse({
                "type": "followers",
                "items": followers,
                "following": following,
                "friends": friends
            })
        else:
            user_auth = get_object_or_404(Node,is_self=True).username
            pass_auth = get_object_or_404(Node,is_self=True).password
            followers = None
            response = None
            try:
                response = requests.get(user.host + "api/authors/" + author_id + "/followers/",timeout=3, auth=HTTPBasicAuth(user_auth, pass_auth))
            except Exception as e:
                print(e)
            if response != None and response.status_code == 200:
                try:
                    followers = response.json()
                    print(followers)
                except JSONDecodeError:
                    print(f"Invalid JSON response from {user.host}: {response.text}")
            else:
                print(f"Request to {user.host} failed")
            # following = requests.request(user.host + "/authors/" + author_id + "/following/")
            # friends = requests.request(user.host + "/authors/" + author_id + "/friends/")
            return JsonResponse({
                "type": "followers",
                "items": followers and followers["items"] or [],
                "following": [],
                "friends": []
            })
    else:
        return HttpResponseBadRequest("Something went wrong!")        

def getFriends(request, author_id=None):
    user = get_object_or_404(User,id=author_id)
    friends = []
    for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True),many=True).data:
        for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True),many=True).data:
            if follower["object"]["id"] == follow["actor"]["id"]:
                friends.append(follower)
    friends = [friend["actor"]["id"] for friend in friends]
    return JsonResponse(friends, safe=False)

class FollowerView(APIView):
    def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')

    def get(self, request, author_id, follower_id):
        """
        check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        """
        ff = get_object_or_404(FollowStatus,actor__id=author_id,obj__id=follower_id,complete=True)
        return Response({"follows": True},status=status.HTTP_200_OK)

    def post(self, request, author_id, follower_id):
        data = json.loads(request.body)
        print("cac", data)
        res = requests.request(method="POST", url=data["object"]["host"] + "api/authors/" + str(follower_id) + "/inbox/",data=request.body)
        if res.status_code == 200:
            if data["type"] == "Follow":
                if not FollowStatus.objects.filter(actor=author_id,obj=follower_id).exists():
                    serializer = SaveFollowSerializer(data={"actor":author_id,"obj":follower_id , "complete": False})
                    if serializer.is_valid():
                        serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            elif data["type"] == "Unfollow":
                item =  get_object_or_404(FollowStatus,actor=author_id,obj=follower_id)
                item.delete()
                return Response(status=status.HTTP_200_OK)
        return Response("NOPE",status=status.HTTP_400_BAD_REQUEST)
    
    # this put is for the notifications page for when you click accept it should go here
    def put(self, request, author_id, follower_id):
        data = json.loads(request.body)
        print("boblb", data)
        res = requests.request(method="POST", url=request.data["actor"]["host"] + "api/authors/" + str(author_id) + "/inbox/",data=request.body)
        if res.status_code == 200:
            req = get_object_or_404(FollowStatus,actor=author_id,obj=follower_id)
            hi_user = User.objects.get(id=follower_id)
            inbox = Inbox.objects.get_or_create(author=hi_user)[0]
            inbox.author = hi_user
            inbox.followRequest.remove(req)
            inbox.save()            
            if data["accepted"]:
                serializer = FollowSerializer(req,data={"complete":True},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                req.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
