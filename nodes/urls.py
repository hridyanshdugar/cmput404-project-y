from django.urls import path
from .views import getNodeDetails, getAllNodeDetails


urlpatterns = [
    path('', getNodeDetails),
    path('all', getAllNodeDetails),
]