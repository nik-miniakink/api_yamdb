from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api_v1.filters import CustomFilterBackend
from .models import Title, Category, Genre, Review, Comment
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer,\
    ReviewDetailSerializer, CommentSerializer
from .permissions import IsAdminOrReadOnly, IsStaffOrAuthorOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [CustomFilterBackend]
    filterset_fields = ['year', 'category', 'genre', 'name']


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class CategoryDestroy(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'slug'


class GenreView(generics.ListCreateAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class GenreDestroy(generics.DestroyAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Title, id=self.kwargs["title_id"])

    def get_queryset(self):
        queryset = Review.objects.filter(title=self.get_post()).all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_post()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def get_post(self):
        get_object_or_404(Title, id=self.kwargs["title_id"])
        return get_object_or_404(Review, id=self.kwargs["review_id"])

    def get_queryset(self):
        queryset = Comment.objects.filter(review=self.get_post()).all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_post()
        )