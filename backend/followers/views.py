from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .helper import body_to_json, addToNewFollowRequestTable
from .models import NewFollowRequest

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

def getNewFollowRequests(request):
    # Get the name
    try:
        name = request.GET['name']
        new_follower_list = NewFollowRequest.objects.filter(name=name).values()
        return JsonResponse(new_follower_list[0])
    except:
        return HttpResponseBadRequest("Something went wrong!")

