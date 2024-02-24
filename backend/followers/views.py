from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, world. from followers")

@csrf_exempt
def follow(request):
    # This is supposed to be a post
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid Request: Please send a post request")
    
    # TODO: Add apikey handling
    
    # Get the request body and send follow request
    print(request.body)
    
    return HttpResponse(request)

