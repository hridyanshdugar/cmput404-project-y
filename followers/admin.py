from django.contrib import admin

# Register your models here.
from .models import Follower, NewFollowRequest, Friends

admin.site.register(Follower)
admin.site.register(NewFollowRequest)
admin.site.register(Friends)