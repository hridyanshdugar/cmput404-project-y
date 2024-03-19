from django.urls import path, re_path
from . import views
from .views import FollowerView
app_name = 'followers'
urlpatterns = [
    re_path(r'^(?P<author_id>.+)/followers/(?P<follower_id>.+)/$', FollowerView.as_view(), name= "/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}"),
    path("<str:author_id>/followers/", views.getFollowers, name= "/authors/\{AUTHOR_ID\}/followers"),
    path("follow/", views.follow, name="follow"),
    path("get/new/follow/requests", views.getNewFollowRequests, name="getNewFollowRequests"),
    path("get/followers", views.getFollowers, name= "getFollowers"),
    path("get/friends", views.getFriends, name= "getFriends"), # /followers/get/friends?name=[email here]
    path("accept/follow/request/", views.acceptFollowRequest, name= "acceptFollowRequest"),
    path("decline/follow/request/", views.declineFollowRequest, name= "declineFollowRequest"),
    path("unfollow/", views.unfollow, name="unfollow")
]
