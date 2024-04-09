from json import JSONDecodeError
from urllib.request import HTTPBasicAuthHandler
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from backend.permissions import RemoteOrSessionAuthenticated
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
import copy 

def getFollowers(request, author_id=None):
    # user = list(User.objects.filter(id=author_id).values())[0]
    if User.objects.filter(id=author_id).exists():
        user = User.objects.get(id=author_id)
        if user.host == Node.objects.get(is_self=True).url:

            try:
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
                    if follower["actor"]["id"] == follow["object"]["id"]:
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
            followers = None
            response = None
            try:
                auth = Node.objects.get(url = user.host)
                response = requests.get(user.host + "api/authors/" + author_id + "/followers",timeout=3, auth=HTTPBasicAuth(auth.username, auth.password))
            except Exception as e:
                print(e)
            if response != None and response.ok:
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
                "following": "following" in followers and followers["following"] or [],
                "friends": "friends" in followers and followers["friends"] or []
            })
    else:
        return HttpResponseBadRequest("Something went wrong!")        

def getFriends(request, author_id):
    user = get_object_or_404(User,id=author_id)
    friends = []
    for follower in FollowSerializer(FollowStatus.objects.filter(obj__id=author_id, complete=True),many=True).data:
        for follow in FollowSerializer(FollowStatus.objects.filter(actor__id=author_id, complete=True),many=True).data:
            if follower["actor"]["id"] == follow["object"]["id"]:
                friends.append(follower)
    friends = [friend["actor"]["id"].split("/")[-1] for friend in friends]
    return JsonResponse(friends, safe=False)

class FollowerView(APIView):
    permission_classes = [ RemoteOrSessionAuthenticated ]

    def get(self, request, author_id, follower_id):
        """
        check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        """
        ff = None
        print("Start")
        if User.objects.filter(id=author_id).exists():
            user = User.objects.get(id=author_id)
            print(user, user.host, "guy")
            ff = FollowSerializer(get_object_or_404(FollowStatus,actor__id=follower_id,obj__id=author_id)).data
            # if user.host == Node.objects.get(is_self=True).url:
            #     print("GOT HERE", author_id, follower_id)
            # else:
            #     auth = Node.objects.get(url = user.host)
            #     try:
            #         response = requests.get(user.host + "api/authors/" + author_id + "/followers/" + follower_id,timeout=3, auth=HTTPBasicAuth(auth.username, auth.password))
            #     except Exception as e:
            #         print(e, "wwhy")
            #     print(response, "response")
            #     if response != None and response.ok:
            #         print("this hit")
            #         try:
            #             ff = response.json()
            #             print(ff, "help me")
            #         except JSONDecodeError:
            #             print(f"Invalid JSON response from {user.host}: {response.text}")
            #     else:
            #         print(f"Request to {user.host} failed")
        if ff:
            return Response(ff,status=status.HTTP_200_OK)
        else:
            return HttpResponseBadRequest("Something went wrong!") 

    def post(self, request, author_id, follower_id):
        """
        Add or remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
        """
        data = request.data
        print("cac", data)
        auth = Node.objects.get(url = data["object"]["host"])
        res = requests.request(method="POST", headers={'Content-Type': 'application/json'}, url=data["object"]["host"] + "api/authors/" + str(author_id) + "/inbox",data=json.dumps(data), auth=HTTPBasicAuth(auth.username, auth.password))
        print(res, "IDK")
        if res.ok:
            if data["type"] == "Follow":
                if not FollowStatus.objects.filter(actor__id=follower_id,obj__id=author_id).exists():
                    serializer = SaveFollowSerializer(data={"actor":follower_id,"obj":author_id , "complete": False})
                    if serializer.is_valid():
                        serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return HttpResponseBadRequest("Already Requested")
            elif data["type"] == "Unfollow":
                item =  get_object_or_404(FollowStatus,actor__id=follower_id,obj__id=author_id)
                item.delete()
                return Response(status=status.HTTP_200_OK)
        return Response("NOPE",status=status.HTTP_400_BAD_REQUEST)
    
    # this put is for the notifications page for when you click accept it should go here
    def put(self, request, author_id, follower_id):
        """
        Accept or decline a follow request from FOREIGN_AUTHOR_ID to AUTHOR_ID
        """
        data = copy.deepcopy(request.data)
        data["actor"] = request.data["object"]
        data["object"] = request.data["actor"]
        print("boblb", data)
        auth = Node.objects.get(url = data["object"]["host"])
        print("boblb 1")
        res = requests.request(method="POST", headers={'Content-Type': 'application/json'}, url=data["object"]["host"] + "api/authors/" + str(follower_id) + "/inbox",data=json.dumps(data), auth=HTTPBasicAuth(auth.username, auth.password))
        print("boblb 2")
        if res.ok:
            print("sent to actor inbox")
            req = get_object_or_404(FollowStatus,actor__id=follower_id,obj__id=author_id)
            hi_user = User.objects.get(id=author_id)
            inbox = Inbox.objects.get_or_create(author=hi_user)[0]
            inbox.followRequest.remove(req)
            inbox.save()            
            if data["accepted"]:
                print("accepted")
                serializer = FollowSerializer(req,data={"complete":True},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                print("declined")
                req.delete()
                return Response(status=status.HTTP_200_OK)
        print("boblb 55 ", res.text)
        return Response(status=status.HTTP_400_BAD_REQUEST)
