from django.db import models

# Constants
USERNAME_MAX_LENGTH = 100
URL_MAX_LENGTH = 300

# Create your models here.
class Follower(models.Model):
    name = models.CharField(max_length=USERNAME_MAX_LENGTH)  # Need to set max user length
    follower = models.CharField(max_length=USERNAME_MAX_LENGTH)
    followerUrl = models.CharField(max_length=URL_MAX_LENGTH)

class NewFollowRequest(models.Model):
    name = models.CharField(max_length=USERNAME_MAX_LENGTH)  # Need to set max user length
    follower = models.CharField(max_length=USERNAME_MAX_LENGTH)
    followerUrl = models.CharField(max_length=URL_MAX_LENGTH)