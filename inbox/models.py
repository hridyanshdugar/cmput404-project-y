import copy
from django.db import models
from posts.models import Post
import uuid

from users.models import User
from users.serializers import RemoteUserSerializer
from users.views import download_profile

TEXT_MAX_LENGTH = 300
class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.OneToOneField("users.User", on_delete=models.CASCADE, null=True)
    post = models.ManyToManyField("posts.Post", blank=True, symmetrical=False)
    followRequest = models.ManyToManyField("followers.FollowStatus", blank=True, symmetrical=False)
    postLikes = models.ManyToManyField("likes.PostLike", blank=True, symmetrical=False)
    comment = models.ManyToManyField("comments.Comment", blank=True, symmetrical=False)
    

def get_foreign_user(data):
    print("beacon 1")
    response_data = copy.deepcopy(data)
    response_data['id'] = response_data['id'].split("/")[-1]
    # updates existing user
    try:
        obj_user = User.objects.get(id=response_data["id"].split("/")[-1])
        print("beacon supreme", obj_user)
        hasPfp = False
        if "profileImage" in response_data:
            hasPfp = response_data.pop("profileImage")
        if "profileBackgroundImage" in response_data:
            ffff = response_data.pop("profileBackgroundImage")

        
        serializer = RemoteUserSerializer(obj_user,data=response_data,partial=True)
        if serializer.is_valid():
            user = serializer.save()
            if hasPfp:
                download_profile(user, hasPfp)
                response_data['profileImage'] = hasPfp
        else:
            print(f"Invalid data from : {serializer.errors}")
    # downloads new user
    except Exception as e:
        print("beacon 2,e", e)

        hasPfp = False
        if "profileImage" in response_data:
            hasPfp = response_data.pop("profileImage")
        if "profileBackgroundImage" in response_data:
                ffff = response_data.pop("profileImage")                    
        print("beacon 3", response_data)
        serializer = RemoteUserSerializer(data=response_data)
        print("beacon 4")
        if serializer.is_valid():
            user = serializer.save()
            if hasPfp:
                download_profile(user, hasPfp)
                response_data['profileImage'] = hasPfp
        else:
            print(f"Invalid data from : {serializer.errors}")

        print("beacon 5")