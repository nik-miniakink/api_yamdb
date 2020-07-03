
from django.urls import path

from .views import CustomUserListView, SpecificUserViewSet, MeUserViewSet

urlpatterns = [
    path('me/', MeUserViewSet.as_view()),
    path('<username>/', SpecificUserViewSet.as_view()),
    path('', CustomUserListView.as_view()),
]
