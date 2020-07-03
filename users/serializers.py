from rest_framework import serializers

from .models import CustomUser


class CustomuserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = CustomUser


class CustomUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'bio', 'role')


class SpecificUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')


class MeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'bio', 'role')