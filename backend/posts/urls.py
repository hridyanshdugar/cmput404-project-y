from django.urls import path
from .views import PostsView, PostsViewPK


urlpatterns = [
    # use the matching view in views.py
    path('', PostsView.as_view()),
    path('<str:pk>', PostsViewPK.as_view())
]