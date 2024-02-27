import uuid
from django.db import models

# Constants
TEXT_MAX_LENGTH = 300
CHOICES_MAX_LENGTH = 8
VISIBILITY_CHOICES = [(1, "PUBLIC"), (2, "FRIENDS"), (3, "UNLISTED")]

class Post(models.Model):
    title = models.CharField(max_length=TEXT_MAX_LENGTH, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    source = models.URLField(max_length=TEXT_MAX_LENGTH)
    origin = models.URLField(max_length=TEXT_MAX_LENGTH)
    description = models.TextField(blank=True, null=True)
    contentType = models.CharField(max_length=TEXT_MAX_LENGTH)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(choices=VISIBILITY_CHOICES, max_length=CHOICES_MAX_LENGTH, default="PUBLIC")
