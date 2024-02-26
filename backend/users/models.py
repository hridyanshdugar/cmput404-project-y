from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

class User(AbstractBaseUser):
    email=models.CharField(max_length=100, blank=False, null=False, unique=True)
    password=models.CharField(max_length=100, blank=False, null=False)
    is_superuser=models.BooleanField(default=False)

    profileImage=models.TextField(blank=True,default='')
    github=models.TextField(blank=True,default='')
    displayName=models.TextField(blank=True,default='')
    approved=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email