from django.db import models

# Constants
USERNAME_MAX_LENGTH = 100
URL_MAX_LENGTH = 300

# Create your models here.
class FollowStatus(models.Model):
    actor = models.ForeignKey('users.User', on_delete=models.CASCADE)
    obj = models.ForeignKey('users.User', on_delete=models.CASCADE)
    # Following status
    # - Pending
    # - Confirmed
    complete=models.BooleanField(default=False)
