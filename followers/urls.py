from django.urls import path, re_path
from . import views
from .views import FollowerView
app_name = 'followers'
urlpatterns = [
    path("<str:author_id>/followers/<str:follower_id>/", FollowerView.as_view()),
    path("<str:author_id>/followers/", views.getFollowers),
    path("get/friends", views.getFriends, name= "getFriends"), 
]
