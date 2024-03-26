from django.urls import path, re_path
from . import views
from .views import FollowerView, AllFollowerView
app_name = 'followers'
urlpatterns = [
    re_path(r'^all/(?P<author_id>.+)/followers/(?P<follower_id>.+)/$', AllFollowerView.as_view(), name= "/authors/all/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}"),
    re_path(r'^(?P<author_id>.+)/followers/(?P<follower_id>.+)/$', FollowerView.as_view(), name= "/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}"),
    path("<str:author_id>/followers/", views.getFollowers, name= "/authors/\{AUTHOR_ID\}/followers"),
    path("<str:author_id>/requests/", views.getNewFollowRequests, name="getNewFollowRequests"),
    path("get/friends", views.getFriends, name= "getFriends"), 
    path("<str:author_id>/decline/<str:follower_id>/", views.declineFollowRequest, name= "declineFollowRequest"),
    path("<str:author_id>/unfollow/<str:follower_id>/", views.unfollow, name="unfollow")
]
