from django.urls import path, re_path
from . import views
from .views import FollowerView, AllFollowerView
app_name = 'followers'
urlpatterns = [
    path("all/<str:author_id>/followers/<str:follower_id>/", AllFollowerView.as_view()),
    path("<str:author_id>/followers/<str:follower_id>/", FollowerView.as_view()),
    path("<str:author_id>/followers/", views.getFollowers),
    path("<str:author_id>/requests/", views.getNewFollowRequests, name="getNewFollowRequests"),
    path("get/friends", views.getFriends, name= "getFriends"), 
    path("<str:author_id>/decline/<str:follower_id>/", views.declineFollowRequest, name= "declineFollowRequest"),
    path("<str:author_id>/unfollow/<str:follower_id>/", views.unfollow, name="unfollow")
]
