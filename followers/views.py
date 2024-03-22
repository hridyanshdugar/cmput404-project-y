from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from users.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from .helper import body_to_json, addToNewFollowRequestTable, addToFollowerTable
from .models import NewFollowRequest, Follower, Friends
from rest_framework.views import APIView
from django.db import transaction
from urllib.parse import unquote
import requests
from django.forms.models import model_to_dict

val = URLValidator()

# @api_view(['POST'])
# @authentication_classes([])
# @permission_classes((AllowAny,))
# def follow(request):
#     # This is supposed to be a post
#     if request.method != "POST":
#         return HttpResponseBadRequest("Invalid Request: Please send a post request")
    
#     # Get the request body and send follow request
#     body = body_to_json(request.body)

#     # Verify the url
#     try:
#         val(body['url'])
#     except ValidationError as e:
#          return HttpResponseBadRequest("Invalid Request: Invalid url")

#     # Add to table
#     addToNewFollowRequestTable(body)

#     return HttpResponse()

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
    user = list(User.objects.filter(id=author_id).values())[0]
    if user:
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
            "followers": followers,
            "following": following,
            "friends": friends
        })
    else:
        return Http404()

def getFriends(request, author_id=None):
    user = list(User.objects.filter(id=author_id).values())[0]
    if user:
        friends = [friend.friendId for friend in Friends.objects.filter(userId=author_id)]
        return JsonResponse(friends, safe=False)
    else:
        return JsonResponse()

# @api_view(['PUT'])
# @authentication_classes([])
# @permission_classes((AllowAny,))
# # Deprecated
# def acceptFollowRequest(request):
#     body = body_to_json(request.body)
#     if request.method != "PUT":
#         return HttpResponseBadRequest("Invalid Request: Please send a put request")
    
#     try:
#         name = body['name']
#         follower = body['follower']
#         url = list(NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower)))[0]
#         url = url["followerUrl"]

#         # Check if the follow request is not already accepted
#         follows = True if list(Follower.objects.filter(Q(name=name) & Q(follower=follower))) else False
#         newRequest = True if list(NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower))) else False

#         if not follows and newRequest:
#             addToFollowerTable(name=name, follower=follower, url=url)
#             NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower)).delete()
#             return HttpResponse()
#         else:
#             NewFollowRequest.objects.filter(Q(name=name) & Q(follower=follower)).delete()
#             return HttpResponseBadRequest("Not able to follow, follows="+ str(follows) + " newRequest=" + str(newRequest)) 
#     except:
#         return HttpResponseBadRequest("Something went wrong!") 

@api_view(['PUT'])
@authentication_classes([])
@permission_classes((AllowAny,))
def declineFollowRequest(request, author_id, follower_id):
    try:
        # Check if the follow request is not already accepted
        follows = True if list(Follower.objects.filter(Q(userId=author_id) & Q(followerId=follower_id))) else False
        newRequest = True if list(NewFollowRequest.objects.filter(Q(userId=author_id) & Q(followerId=follower_id))) else False

        if not follows and newRequest:
            NewFollowRequest.objects.filter(Q(userId=author_id) & Q(followerId=follower_id)).delete()
            return HttpResponse()
        else:
            NewFollowRequest.objects.filter(Q(userId=author_id) & Q(followerId=follower_id)).delete()
            return HttpResponseBadRequest("Not able to decline request, follows="+ str(follows) + " newRequest=" + str(newRequest)) 
    except:
        return HttpResponseBadRequest("Something went wrong!") 




class FollowerView(APIView):

    def delete(self, request, author_id, follower_id):
        """
        remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID, basically same functionality as unfollow
        """
        follows = True if list(Follower.objects.filter(Q(userId=author_id) & Q(followerId=follower_id)).values()) else False
        if follows:
            Friends.objects.filter(Q(userId=author_id) & Q(friendId=follower_id)).delete()
            Friends.objects.filter(Q(userId=follower_id) & Q(friendId=author_id)).delete()
            Follower.objects.filter(Q(userId=author_id) & Q(followerId=follower_id)).delete()
        return HttpResponse("Deleted/Unfollowed")

    def get(self, request, author_id, follower_id):
        """
        check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID
        """
        follows = True if list(Follower.objects.filter(Q(userId=author_id) & Q(followerId=follower_id))) else False
        if follows:
            return JsonResponse({"follows": follows})
        else:
            return HttpResponse(status=404)

    def put(self, request, author_id, follower_id):
        """
        Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID, basically same functionality as accept Follow request
        """
        try:
            # Check if the follow request is not already accepted
            follows = True if list(Follower.objects.filter(Q(userId=author_id) & Q(followerId=follower_id))) else False
            newRequest = True if list(NewFollowRequest.objects.filter(Q(userId=author_id) & Q(followerId=follower_id))) else False

            if not follows and newRequest:
                req = list(NewFollowRequest.objects.filter(Q(userId=author_id) & Q(followerId=follower_id)).values())[0]
                Follower.objects.create(userId=req["userId"], 
                                        followerId=req["followerId"], 
                                        host=req["host"],
                                        displayName=req["displayName"],
                                        url=req["url"],
                                        github=req["github"],
                                        profileImage=req["profileImage"])
                NewFollowRequest.objects.filter(Q(userId=author_id) & Q(followerId=follower_id)).delete()
                # Check if friend, if yes then add to table
                friend = True if len(list(Follower.objects.filter((Q(userId=follower_id) & Q(followerId=author_id))))) == 1 else False
                if friend:
                    Friends.objects.create(userId=req["userId"],
                                           friendId=req["followerId"],
                                           host=req["host"],
                                           displayName=req["displayName"],
                                           url=req["url"],
                                           github=req["github"],
                                           profileImage=req["profileImage"])
                    Friends.objects.create(userId=req["followerId"],
                                           friendId=req["userId"],
                                           host=req["host"],
                                           displayName=req["displayName"],
                                           url=req["url"],
                                           github=req["github"],
                                           profileImage=req["profileImage"])
                return HttpResponse()
            else:
                NewFollowRequest.objects.filter(Q(userId=author_id) & Q(followerId=follower_id)).delete()
                return HttpResponseBadRequest("Not able to follow, follows="+ str(follows) + " newRequest=" + str(newRequest)) 
        except:
            return HttpResponseBadRequest("Something went wrong!")
