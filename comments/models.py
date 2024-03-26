from django.db import models
from posts.models import Post
import uuid

TEXT_MAX_LENGTH = 300
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    contentType = models.CharField(max_length=TEXT_MAX_LENGTH)
    comment = models.TextField(blank=False, null=False)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)