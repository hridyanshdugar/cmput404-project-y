from django.urls import path
from . import views

app_name = 'followers'
urlpatterns = [
    path("", views.index, name="index"),
    path("follow/", views.follow, name="follow"),
    path("get/new/follow/requests", views.getNewFollowRequests, name="getNewFollowRequests")
]
