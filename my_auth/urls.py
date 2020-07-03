from django.urls import path, include

from .views import GenerateConfirmationCode, MyTokenObtainPairView


urlpatterns = [
    path('mail/', GenerateConfirmationCode.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

]
