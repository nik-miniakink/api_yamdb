from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Verificate
from users.models import CustomUser




class VerificateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()

    class Meta:
        fields = ('email', 'confirmation_code')
        model = Verificate


class MyTokenObtainPairSerializer(serializers.Serializer):

    def validate(self, data):
        email = self.context['request'].data.get('email')
        new_user = get_object_or_404(CustomUser, email=email)
        refresh = self.get_token(new_user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
