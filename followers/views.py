from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from users.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from .helper import body_to_json, addToNewFollowRequestTable, addToFollowerTable
from .models import NewFollowRequest, Follower

val = URLValidator()

def index(request):
    return HttpResponse("Hello, world. from followers")

@api_view(['POST'])
@authentication_classes([])
@permission_classes((AllowAny,))
def follow(request):
    # This is supposed to be a post
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid Request: Please send a post request")
    
    # Get the request body and send follow request
    body = body_to_json(request.body)

    # Verify the url
    try:
        val(body['url'])
    except ValidationError as e:
         return HttpResponseBadRequest("Invalid Request: Invalid url")

    # Add to table
    addToNewFollowRequestTable(body)

    return HttpResponse()

@api_view(['POST'])
@authentication_classes([])
@permission_classes((AllowAny,))
def unfollow(request):
    # This is supposed to be a post
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid Request: Please send a put request with author 'name' and 'follower' name as headers")

    body = body_to_json(request.body)

    # delete from followers table
    try:
        Follower.objects.filter(Q(follower=body['friend']) & Q(name= body['name'])).delete()
    except:
        return HttpResponseBadRequest("Invalid Request: Follower not found, are you sending 'name' and 'follower' in the headers")

    return HttpResponse()

def getNewFollowRequests(request):
    # Get the name
    try:
        name = request.GET['name']
        new_follower_list = list(NewFollowRequest.objects.filter(name=name).values())
        users = []
        for new_follower in new_follower_list:
            user = list(User.objects.filter(email=new_follower["follower"]).values())[0]
            users.append(user)
        return JsonResponse(users, safe=False)
    except:
        return HttpResponseBadRequest("Something went wrong!")

def getFollowers(request):
    try:
        name = request.GET['name']
        new_follower_list = list(Follower.objects.filter(name=name).values())
        users = []
        for new_follower in new_follower_list:
            user = list(User.objects.filter(email=new_follower["follower"]).values())[0]
            users.append(user)
        return JsonResponse(users, safe=False)
    except:
        return HttpResponseBadRequest("Something went wrong!")    

def getFriends(request):
    try:
        name = request.GET['name']
        new_friend_list = list(Follower.objects.filter(name=name).values())
        names = set()
        for follower in new_friend_list:
            follower_follow_list = list(Follower.objects.filter(name=follower["follower"]).values())
            for follower_follower in follower_follow_list:
                print(follower, follower_follower)
                if follower_follower["name"] == follower["follower"] and follower_follower["follower"] == follower["name"]:
                    names.add(follower_follower["name"])
        users=[]  
        for name in names:
            user = list(User.objects.filter(email=name).values())[0]
            users.append(user)
        return JsonResponse(users, safe=False)
    except:
        return HttpResponseBadRequest("Something went wrong!")  

@api_view(['PUT'])
@authentication_classes([])
@permission_classes((AllowAny,))
def acceptFollowRequest(request):
    body = body_to_json(request.body)
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid Request: Please send a put request")
    
    try:
        name = body['name']
        follower = body['follower']
        url = "testurl"
        # Check if the follow request is not already accepted
        follows = True if list(Follower.objects.filter(Q(name=name) & Q(follower=follower))) else False
        newRequest = True if list(NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower))) else False

        if not follows and newRequest:
            addToFollowerTable(name=name, follower=follower, url=url)
            NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower)).delete()
            return HttpResponse()
        else:
            NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower)).delete()
            return HttpResponseBadRequest("Not able to follow, follows="+ str(follows) + " newRequest=" + str(newRequest)) 
    except:
        return HttpResponseBadRequest("Something went wrong!") 

@api_view(['PUT'])
@authentication_classes([])
@permission_classes((AllowAny,))
def declineFollowRequest(request):
    body = body_to_json(request.body)
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid Request: Please send a put request")
    try:
        name = body['name']
        follower = body['follower']

        # Check if the follow request is not already accepted
        follows = True if list(Follower.objects.filter(Q(name=name) & Q(follower=follower))) else False
        newRequest = True if list(NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower))) else False

        if not follows and newRequest:
            NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower)).delete()
            return HttpResponse()
        else:
            NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower)).delete()
            return HttpResponseBadRequest("Not able to decline request, follows="+ str(follows) + " newRequest=" + str(newRequest)) 
    except:
        return HttpResponseBadRequest("Something went wrong!") 

