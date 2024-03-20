from django.db import models
from posts.models import Post
import uuid

TEXT_MAX_LENGTH = 300
class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    global_id = models.CharField(max_length=TEXT_MAX_LENGTH,unique=True)
    
    type = models.URLField(max_length=TEXT_MAX_LENGTH,default='')
    author = models.OneToOneField("users.User", on_delete=models.CASCADE)
    post = models.ManyToManyField("posts.Post", blank=True, symmetrical=False)
    follow = models.ManyToManyField("followers.NewFollowRequest", blank=True, symmetrical=False)
    like = models.ManyToManyField("likes.Like", blank=True, symmetrical=False)
    comment = models.ManyToManyField("comments.Comment", blank=True, symmetrical=False)
    