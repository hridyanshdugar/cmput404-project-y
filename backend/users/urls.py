from django.urls import path
from .views import UsersViewPK, UsersView


urlpatterns = [
    # use the matching view in views.py
    path('', UsersView.as_view()),
    path('<int:pk>', UsersViewPK.as_view())
]