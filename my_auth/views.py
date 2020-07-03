import random

from django.conf import settings
from django.core.mail import send_mail

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Verificate
from .serializers import VerificateSerializer, MyTokenObtainPairSerializer
from users.models import CustomUser


class GenerateConfirmationCode(generics.CreateAPIView):
    """
    Generate confirmation code and sent it to email
    """
    serializer_class = VerificateSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        email = self.request.data['email']
        emails = Verificate.objects.filter(email=email)
        if emails is not None:
            emails.delete()
        confirmation_code = str(random.randint(10000, 99999))
        send_mail(
            'Confirmation code',
            f'Your one-time confirmation code {confirmation_code}',
            settings.EMAIL_HOST_USER,
            [f'{email}']
        )

        serializer.save(email=email, confirmation_code=confirmation_code)

    def get_queryset(self):
        email = self.request.data['email']
        queryset = Verificate.objects.filter(email=email)
        return queryset


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Sends a token by email and confirmation
    """
    serializer_class = MyTokenObtainPairSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')
        if not email:
            return Response("Email is required field.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not confirmation_code:
            return Response("Confirmation code is required field.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not Verificate.objects.filter(email=email,
                                       confirmation_code=confirmation_code):
            return Response("Confirmation code for your email isn't valid.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not CustomUser.objects.filter(email=email):
            CustomUser.objects.create(email=email)
        if serializer.is_valid(raise_exception=True):
            Verificate.objects.get(email=email).delete()
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)
