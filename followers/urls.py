from django.urls import path
from . import views

app_name = 'followers'
urlpatterns = [
    path("", views.index, name="index"),
    path("follow/", views.follow, name="follow"),
    path("get/new/follow/requests", views.getNewFollowRequests, name="getNewFollowRequests"),
    path("get/followers", views.getFollowers, name= "getFollowers"),
    path("accept/follow/request/", views.acceptFollowRequest, name= "acceptFollowRequest"),
    path("decline/follow/request/", views.declineFollowRequest, name= "declineFollowRequest"),
    path("unfollow/", views.unfollow, name="unfollow")
]
