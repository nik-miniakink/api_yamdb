from django.shortcuts import get_object_or_404

from rest_framework import serializers

from api_v1 import serializer_fields
from .models import Title, Category, Genre, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate(self, attrs):
        slug = self.context['request'].data.get('slug')
        if not slug:
            raise serializers.ValidationError(
                f"Slug is the requirement field.")
        if Genre.objects.filter(slug=slug):
            raise serializers.ValidationError(
                f"Category with this slug already exist.")
        return attrs


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate(self, attrs):
        slug = self.context['request'].data.get('slug')
        if not slug:
            raise serializers.ValidationError(
                f"Slug is the requirement field.")
        if Genre.objects.filter(slug=slug):
            raise serializers.ValidationError(
                f"Genre with this slug already exist.")
        return attrs


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')
    category = serializer_fields.CategorySlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializer_fields.GenreSlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    @staticmethod
    def get_rating(obj):
        title_id = obj.id
        reviews = Review.objects.filter(title=title_id)
        if reviews:
            total_rating = [review.score for review in reviews]
            avg_rating = sum(total_rating) / len(total_rating)
            return avg_rating


class ReviewDetailSerializer(serializers.ModelSerializer):
    author = serializer_fields.AuthorSlugRelatedField(slug_field='id',
                                                      read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        method = self.context['request'].method
        if Review.objects.filter(author=self.context['request'].user,
                                 title=self.get_title()) and method != 'PATCH':
            raise serializers.ValidationError(
                f"You  have already created review on this title.")
        return attrs

    def get_title(self):
        title = get_object_or_404(Title, id=self.context.get('view').kwargs.get(
            'title_id'))
        return title


class CommentSerializer(serializers.ModelSerializer):
    author = serializer_fields.AuthorSlugRelatedField(slug_field='id',
                                                      read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
