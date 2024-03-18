from django.urls import path
from .views import CommentsView, CommentsViewPK

urlpatterns = [
    # use the matching view in views.py
    path('', CommentsView.as_view()),
    path('<uuid:pk>', CommentsViewPK.as_view())
]