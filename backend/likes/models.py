from django.db import models
from posts.models import Post
import uuid

TEXT_MAX_LENGTH = 300
class CommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    global_id = models.CharField(max_length=TEXT_MAX_LENGTH,unique=True)
    
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    