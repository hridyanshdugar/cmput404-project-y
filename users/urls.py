from django.urls import path
from .views import UsersViewPK, UsersView, AllUsersView


urlpatterns = [
    # use the matching view in views.py
    path('', UsersView.as_view()),
    path('all', AllUsersView.as_view()),
    path('<uuid:pk>', UsersViewPK.as_view())
]