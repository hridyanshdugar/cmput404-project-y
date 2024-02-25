from django.urls import path
from .views import login, signup


urlpatterns = [
    path('login', login),
    path('signup', signup)
    #path('token-auth', token_auth)
]