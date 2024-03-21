from django.db import models

NODE_MAX_LENGTH = 200
class Node(models.Model):
    url = models.CharField(max_length=NODE_MAX_LENGTH,unique=True)
    username = models.CharField(max_length=NODE_MAX_LENGTH)
    password = models.CharField(max_length=NODE_MAX_LENGTH,null=False,blank=False)
    is_self = models.BooleanField(default=False)

