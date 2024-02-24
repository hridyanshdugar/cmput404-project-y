from django.db import models

# Constants
USERNAME_MAX_LENGTH = 100
URL_MAX_LENGTH = 300

# Create your models here.
class Followers(models.Model):
    name = models.CharField(max_length=USERNAME_MAX_LENGTH)  # Need to set max user length
    url = models.CharField(max_length=URL_MAX_LENGTH)

class NewFollowRequests(models.Model):
    name = models.CharField(max_length=USERNAME_MAX_LENGTH)  # Need to set max user length
    url = models.CharField(max_length=URL_MAX_LENGTH)