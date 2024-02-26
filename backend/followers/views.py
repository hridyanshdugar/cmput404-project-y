from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .helper import body_to_json, addToNewFollowRequestTable, addToFollowerTable
from .models import NewFollowRequest, Follower

val = URLValidator()

def index(request):
    return HttpResponse("Hello, world. from followers")

@csrf_exempt
def follow(request):
    # This is supposed to be a post
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid Request: Please send a post request")
    
    # TODO: Add apikey handling
    
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

@csrf_exempt
def unfollow(request):
    # This is supposed to be a post
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid Request: Please send a put request with author 'name' and 'follower' name as headers")
    
    # TODO: Add apikey handling

    # delete from followers table
    try:
        Follower.objects.filter(follower=request.headers['follower'], name= request.headers['name']).delete()
    except:
        return HttpResponseBadRequest("Invalid Request: Follower not found, are you sending 'name' and 'follower' in the headers")

    return HttpResponse()

def getNewFollowRequests(request):
    # Get the name
    try:
        name = request.GET['name']
        new_follower_list = list(NewFollowRequest.objects.filter(name=name).values())
        return JsonResponse(new_follower_list, safe=False)
    except:
        return HttpResponseBadRequest("Something went wrong!")

def getFollowers(request):
    try:
        name = request.GET['name']
        new_follower_list = list(Follower.objects.filter(name=name).values())
        return JsonResponse(new_follower_list, safe=False)
    except:
        return HttpResponseBadRequest("Something went wrong!")    

@csrf_exempt
def acceptFollowRequest(request):
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid Request: Please send a put request")
    
    try:
        name = request.headers['name']
        follower = request.headers['follower']
        url = request.headers['url']
        # Check if the follow request is not already accepted
        follows = True if list(Follower.objects.filter(name=name,follower=follower)) else False
        newRequest = True if list(NewFollowRequest.objects.filter(name=name, follower=follower, followerUrl=url)) else False

        if not follows and newRequest:
            addToFollowerTable(name=name, follower=follower, url=url)
            NewFollowRequest.objects.filter(name=name, follower=follower, followerUrl=url).delete()
            return HttpResponse()
        else:
            return HttpResponseBadRequest("Not able to follow, follows="+ str(follows) + " newRequest=" + str(newRequest)) 
    except:
        return HttpResponseBadRequest("Something went wrong!") 

@csrf_exempt
def declineFollowRequest(request):
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid Request: Please send a put request")
    
    try:
        name = request.headers['name']
        follower = request.headers['follower']
        url = request.headers['url']

        # Check if the follow request is not already accepted
        follows = True if list(Follower.objects.filter(name=name,follower=follower)) else False
        newRequest = True if list(NewFollowRequest.objects.filter(name=name, follower=follower, followerUrl=url)) else False

        if not follows and newRequest:
            NewFollowRequest.objects.filter(name=name, follower=follower, followerUrl=url).delete()
            return HttpResponse()
        else:
            return HttpResponseBadRequest("Not able to decline request, follows="+ str(follows) + " newRequest=" + str(newRequest)) 
    except:
        return HttpResponseBadRequest("Something went wrong!") 