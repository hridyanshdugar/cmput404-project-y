import uuid
from django.db import models

# Constants
TEXT_MAX_LENGTH = 300
CHOICES_MAX_LENGTH = 8
VISIBILITY_CHOICES = [("PUBLIC", "PUBLIC"), ("FRIENDS", "FRIENDS"), ("UNLISTED", "UNLISTED")]

class Post(models.Model):
    title = models.CharField(max_length=TEXT_MAX_LENGTH, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    global_id = models.CharField(null=True, max_length=TEXT_MAX_LENGTH,unique=True)
    host = models.URLField(max_length=TEXT_MAX_LENGTH,default='')
    source = models.URLField(max_length=TEXT_MAX_LENGTH,default='')
    origin = models.URLField(max_length=TEXT_MAX_LENGTH,default='')
    description = models.TextField(blank=True, default='')
    contentType = models.CharField(max_length=TEXT_MAX_LENGTH)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(choices=VISIBILITY_CHOICES, max_length=CHOICES_MAX_LENGTH, default="PUBLIC")

    objects = models.Manager()