from django.db import models
from posts.models import Post
import uuid

TEXT_MAX_LENGTH = 300
class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    type = models.URLField(max_length=TEXT_MAX_LENGTH,default='')
    author = models.OneToOneField("users.User", on_delete=models.CASCADE, null=True)
    post = models.ManyToManyField("posts.Post", blank=True, symmetrical=False)
    followRequest = models.ManyToManyField("followers.FollowStatus", blank=True, symmetrical=False)
    postLikes = models.ManyToManyField("likes.PostLike", blank=True, symmetrical=False)
    commentLikes = models.ManyToManyField("likes.CommentLike", blank=True, symmetrical=False)
    comment = models.ManyToManyField("comments.Comment", blank=True, symmetrical=False)
    