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
from .serializers import FollowSerializer
from .models import FollowStatus

val = URLValidator()

def getNewFollowRequests(request, author_id):
    # Get the name
    try:
        new_follower_list = list(NewFollowRequest.objects.filter(userId=author_id).values())
        users = []
        for new_follower in new_follower_list:
            user = list(User.objects.filter(id=new_follower["followerId"]).values())[0]
            users.append(user)
        return JsonResponse(users, safe=False)
    except:
        return HttpResponseBadRequest("Something went wrong!")

def getFollowers(request, author_id=None):
    # user = list(User.objects.filter(id=author_id).values())[0]
    if User.objects.filter(id=author_id).exists():
        user = User.objects.get(id=author_id)
        if user.host != Node.objects.get(is_self=True).url:
            try:
                print("here")
                followers = [follower["followerId"] for follower in Follower.objects.filter(userId=author_id).values()] 
            except:
                followers = []
            try:
                friends = [friend["friendId"] for friend in Friends.objects.filter(userId=author_id).values()]
            except: 
                friends = []
            try:
                following = [follower["userId"] for follower in Follower.objects.filter(followerId=author_id).values()]
            except:
                following = []
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
    user = list(User.objects.filter(id=author_id).values())[0]
    if user:
        friends = [friend.friendId for friend in Friends.objects.filter(userId=author_id)]
        return JsonResponse(friends, safe=False)
    else:
        return JsonResponse()

class AllFollowerView(APIView):
    def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status= status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')
    
    def get(self, request, author_id, follower_id):
        """
        check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        """
        if Follower.objects.filter(userId=author_id).exists():
            follows = True if Follower.objects.filter(Q(userId=author_id) & Q(followerId=follower_id)).exists() else False
            if follows:
                return JsonResponse({"follows": follows})
            else:
                return JsonResponse({"follows": False})
        else:
            user_auth = get_object_or_404(Node,is_self=True).username
            pass_auth = get_object_or_404(Node,is_self=True).password

            nodes = Node.objects.filter(is_self=False)

            for node in nodes:
                print(node.url + "api/authors/" + str(author_id) + "/followers/" + str(follower_id) + "/")
                try:
                    response = requests.get(node.url + "api/authors/" + str(author_id) + "/followers/" + str(follower_id) + "/", timeout=20,auth=HTTPBasicAuth(user_auth, pass_auth))
                    
                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                            return JsonResponse(response_data)
                        except JSONDecodeError:
                            print(f"Invalid JSON response from {node.url}: {response.text}")
                    else:
                        print(f"Request to {node.url} failed with status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Request to {node.url} failed: {e}")
            return JsonResponse({"follows": False})




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
        ff = get_object_or_404(FollowStatus,actor=author_id,obj=follower_id,complete=True)
        return Response({"follows": True},status=status.HTTP_200_OK)

    def post(self, request, author_id, follower_id):
        res = requests.request(method="POST", url=request.data["object"]["host"] + "api/authors/" + str(follower_id) + "/inbox/",data=request.data)
        if res.status_code == 200:
            if request.data["type"] == "Follow":
                serializer = FollowSerializer(data={"actor":author_id,"obj":follower_id})
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            elif request.data["type"] == "Unfollow":
                item =  get_object_or_404(FollowStatus,actor=author_id,obj=follower_id)
                item.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # this put is for the notifications page for when you click accept it should go here
    def put(self, request, author_id, follower_id):
        res = requests.request(method="POST", url=request.data["object"]["host"] + "api/authors/" + str(follower_id) + "/inbox/",data=request.data)
        if res.status_code == 200:
            req = get_object_or_404(FollowStatus,actor=author_id,obj=follower_id)
            if request.data["accepted"]:
                serializer = FollowSerializer(req,data={"complete":True},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                req.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
