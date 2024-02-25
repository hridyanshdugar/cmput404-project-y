from django.db import models

class Posts(models.Model):
    media = models.ImageField(upload_to=media_upload_path)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
