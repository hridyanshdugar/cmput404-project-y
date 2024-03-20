from django.db import models
from posts.models import Post
from comments.models import Comment
import uuid

TEXT_MAX_LENGTH = 300
class PostLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    summary = models.CharField(max_length=TEXT_MAX_LENGTH,blank=True)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)


class CommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    summary = models.CharField(max_length=TEXT_MAX_LENGTH,blank=True)
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)