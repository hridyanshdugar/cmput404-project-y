from django.urls import path
from .views import UsersViewPK, UsersView


urlpatterns = [
    # use the matching view in views.py
    path('generic', UsersView),
    path('generic/<int:pk>', UsersViewPK)
]