from django.urls import path
from .views import ImageView, ImageViewPK


urlpatterns = [
    # use the matching view in views.py
    path('', ImageView.as_view()),
    path('<uuid:pk>', ImageViewPK.as_view())
]