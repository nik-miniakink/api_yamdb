from django.urls import path, include

from .views import VerificateCode, MyTokenObtainPairView


urlpatterns = [
    path('mail/', VerificateCode.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

]
