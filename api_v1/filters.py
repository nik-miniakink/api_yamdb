from rest_framework import filters
from .models import Category, Genre, Title


class CustomFilterBackend(filters.BaseFilterBackend):
    """
    Search for two fields(year,name) and two related fields(category, genre)
    """
    def filter_queryset(self, request, queryset, view):
        category_slug = request.query_params.get('category')
        genre_slug = request.query_params.get('genre')
        name = request.query_params.get('name')
        year = request.query_params.get('year')

        if Genre.objects.filter(slug=genre_slug).exists():
            queryset = queryset.filter(genre__slug=genre_slug)
        if Category.objects.filter(slug=category_slug).exists():
            queryset = queryset.filter(category__slug=category_slug)
        if queryset.filter(year=year).exists():
            queryset = queryset.filter(year=year)
        if name:
            if Title.objects.filter(name=name):
                queryset = queryset.filter(name__in=self.get_names(name))


        return queryset

    @staticmethod
    def get_names(name):
        return [title.name for title in Title.objects.all() if
                name in title.name]
