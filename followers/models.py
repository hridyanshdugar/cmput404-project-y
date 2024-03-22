from django.db import models

# Constants
USERNAME_MAX_LENGTH = 100
URL_MAX_LENGTH = 300

# Create your models here.
class Friends(models.Model):
    userId = models.TextField(editable=False, unique=False, default='')
    friendId = models.TextField(editable=False, unique=False, default='')
    host=models.TextField(blank=True, default='')
    displayName=models.TextField(blank=True, default='')
    url = models.TextField(blank=True, default='')
    github=models.TextField(blank=True, default='')
    profileImage=models.TextField(blank=True, default='')

class Follower(models.Model):
    userId = models.TextField(editable=False, unique=False, default='')
    followerId = models.TextField(editable=False, unique=False, default='')
    host=models.TextField(blank=True, default='')
    displayName=models.TextField(blank=True, default='')
    url = models.TextField(blank=True, default='')
    github=models.TextField(blank=True, default='')
    profileImage=models.TextField(blank=True, default='')

class NewFollowRequest(models.Model):
    userId = models.TextField(editable=False, unique=False, default='')
    followerId = models.TextField(editable=False, unique=False, default='')
    host=models.TextField(blank=True, default='')
    displayName=models.TextField(blank=True, default='')
    url = models.TextField(blank=True, default='')
    github=models.TextField(blank=True, default='')
    profileImage=models.TextField(blank=True, default='')