from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import uuid
import os

def image_upload_path(instance, filename):
    file_extension = os.path.splitext(filename)
    return os.path.join('image', f'image_{uuid.uuid4()}{file_extension}')

class Image(models.Model):
    image=models.ImageField(upload_to=image_upload_path)

@receiver(post_delete, sender=Image)
def delete_media_on_image_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.profileImage.path):
        os.remove(instance.image.path)
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

@receiver(pre_save, sender=Image)
def delete_media_on_image_save(sender, instance, **kwargs):
    obj = None
    try:
        obj = Image.objects.get(id=instance.id)
    except:
        return False
        
    if instance.image and obj and obj.image and os.path.isfile(obj.image.path) and obj.image != instance.image:
        os.remove(obj.image.path)
    if instance.image and obj and obj.image and os.path.isfile(obj.image.path) and obj.image != instance.image:
        os.remove(obj.image.path)