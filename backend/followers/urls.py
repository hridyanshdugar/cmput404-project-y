from django.urls import path
from .views import FollowersView


urlpatterns = [
    # use the matching view in views.py
    path('<int:pk>', FollowersView.as_view())
]