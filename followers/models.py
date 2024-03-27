from django.db import models

# Constants
USERNAME_MAX_LENGTH = 100
URL_MAX_LENGTH = 300

class FollowStatus(models.Model):
    actor = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='following')
    obj = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='to_follow')
    # Following status
    # - Pending
    # - Confirmed
    complete = models.BooleanField(default=False)