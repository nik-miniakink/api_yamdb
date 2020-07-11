"""YaMDb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, GenreView, GenreDestroy, ReviewViewSet, CommentViewSet, CategoryListCreateView, CategoryDestroy

router = DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('categories/<slug:slug>/', CategoryDestroy.as_view()),
    path('categories/', CategoryListCreateView.as_view()),
    path('genres/<slug:slug>/', GenreDestroy.as_view()),
    path('genres/', GenreView.as_view()),
    path('', include(router.urls)),
]

