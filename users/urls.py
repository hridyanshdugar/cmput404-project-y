from django.urls import path
from .views import UsersViewPK, UsersView, AllUsersView, AllUsersViewPK


urlpatterns = [
    # use the matching view in views.py
    path('', UsersView.as_view()),
    path('all', AllUsersView.as_view()),
    path('all/<uuid:pk>', AllUsersViewPK.as_view()),
    path('<uuid:pk>', UsersViewPK.as_view())
]