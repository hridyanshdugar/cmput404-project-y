from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import pre_save, post_delete
from django.core.files.storage import default_storage
from django.dispatch import receiver
import uuid
import os
from django.contrib.auth.hashers import make_password



class UserManager(BaseUserManager):
    use_in_migration = True
    def create_user(self, email, password, **extra_fields):
        if not email or not password:
            raise ValueError('Email and password is Required')
        
        user = User(email=self.normalize_email(email), password=make_password(password), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
              raise ValueError('Staff attribute must be True')

        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
              raise ValueError('Superuser attribute must be True')


        user = self.create_user(email, password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)

def pfp_upload_path(instance, filename):
    file_extension = os.path.splitext(filename)
    return os.path.join('pfps', f'pfp_{uuid.uuid4()}{file_extension}')

def profilebackground_upload_path(instance, filename):
    file_extension = os.path.splitext(filename)
    return os.path.join('profilebackgrounds', f'profilebackground_{uuid.uuid4()}{file_extension}')

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    url=models.TextField(blank=True,default='')
    host=models.TextField(blank=True,default='')

    email=models.CharField(max_length=100, blank=False, null=False, unique=True)
    password=models.CharField(max_length=100, blank=False, null=False)

    is_superuser=models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    profileImage=models.ImageField(null=True,upload_to=pfp_upload_path)
    profileBackgroundImage=models.ImageField(null=True,upload_to=profilebackground_upload_path)
    github=models.TextField(blank=True,default='')
    displayName=models.TextField(blank=True,default='')
    approved=models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()

    def __str__(self):
        return self.email

@receiver(post_delete, sender=User)
def delete_media_on_user_delete(sender, instance, **kwargs):
    if instance.profileImage:
        instance.profileImage.delete()
    if instance.profileBackgroundImage:
        instance.profileBackgroundImage.delete()

@receiver(pre_save, sender=User)
def delete_media_on_user_save(sender, instance, **kwargs):
    obj = None
    try:
        obj = User.objects.get(id=instance.id)
    except:
        return False
        
    if instance.profileImage and obj and obj.profileImage and obj.profileImage != instance.profileImage:
        obj.profileImage.delete()
    if instance.profileBackgroundImage and obj and obj.profileBackgroundImage and obj.profileBackgroundImage != instance.profileBackgroundImage:
        obj.profileBackgroundImage.delete()