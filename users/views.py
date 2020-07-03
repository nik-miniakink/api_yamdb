from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .permission import IsAdmin
from .serializers import CustomuserSerializer, CustomUsernameSerializer, MeUserSerializer


class CustomUserListView(generics.ListCreateAPIView):
    serializer_class = CustomuserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        username = self.request.query_params.get('search', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset


class SpecificUserViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUsernameSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.queryset.get(username=self.kwargs["username"])


class MeUserViewSet(generics.RetrieveUpdateAPIView, generics.ListAPIView):
    serializer_class = MeUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user
