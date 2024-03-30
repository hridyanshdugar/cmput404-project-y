"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from index.views import main
from userauth import urls
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView
from likes.views import PostLikesViewPK, PostLikesView, CommentLikesViewPK
from inbox.views import InboxView
from users.views import UsersViewPK
from followers.views import FollowerView, getFollowers
from posts.views import AllPostsView, AllPostsView2, PostsView, PostsViewPK

heroku_react_django_urls = [
    re_path('.*', TemplateView.as_view(template_name='index.html', content_type='text/html'))
]

urlpatterns = [
    path('api/', include([
        path('admin/', admin.site.urls),
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('authors/all/<str:author_id>/posts/', AllPostsView.as_view()),
        path('authors/all/<str:author_id>/posts2/', AllPostsView2.as_view()),
        path('authors/<str:author_id>/posts/<uuid:fk>/comments/', include('comments.urls')),
        path('posts/', include('posts.urls')),
        path('authors/<str:author_id>/posts/<str:post_id>', PostsViewPK.as_view()),
        path('authors/<str:author_id>/posts/', PostsView.as_view()),
        path('nodes/', include('nodes.urls')),
        path('auth/', include('userauth.urls')),
        path('users/', include('users.urls')),
        path('images/', include('image.urls')),
        path('followers/', include('followers.urls')),
        path('authors/<str:author_id>/posts/<str:post_id>/likes', PostLikesViewPK.as_view()),
        path('authors/<str:author_id>/comments/<str:post_id>/likes', CommentLikesViewPK.as_view()),
        path('authors/<str:author_id>/liked', PostLikesView.as_view()),
        path('authors/<str:pk>/', UsersViewPK.as_view()),
        path('authors/<str:author_id>/followers/<str:follower_id>/', FollowerView.as_view()),
        path('authors/all/<str:author_id>/followers/<str:follower_id>/', FollowerView.as_view()),
        path("authors/<str:author_id>/followers/", getFollowers),
        # path('authors/', include('followers.urls')),
        path('authors/<str:pk>/inbox/', InboxView.as_view()),
        # path('authors/<str:author_id>/posts/<uuid:fk>/likes', include('likes.urls')),
        # path('authors/<str:author_id>/posts/<uuid:fk>/comments/<uuid:ck>/likes', include('likes.urls')),
    ])),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.LOCAL_SERVE_MEDIA_FILES:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += heroku_react_django_urls