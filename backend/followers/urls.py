from django.urls import path
from . import views

app_name = 'followers'
urlpatterns = [
    path("", views.index, name="index"),
]
