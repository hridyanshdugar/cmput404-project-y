from django.urls import path
from .views import PostsView, PostsViewPK, AllPostsView

urlpatterns = [
    # use the matching view in views.py
    path('', PostsView.as_view()),
    path('all/<uuid:pk>', AllPostsView.as_view()),
    path('<uuid:pk>', PostsViewPK.as_view())
]