from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Title(models.Model):
    """
    Product Information
    """
    name = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, default=0)
    description = models.CharField(blank=True, null=True, max_length=300)
    genre = models.ManyToManyField('Genre', blank=True, related_name="titles")
    category = models.ForeignKey('Category', blank=True, null=True,
                                 on_delete=models.DO_NOTHING,
                                 related_name="titles")

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Category Information
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Information from the reviews
    """
    title = models.ForeignKey(Title, on_delete=models.DO_NOTHING,
                              related_name="reviews")
    text = models.TextField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name="reviews")
    pub_date = models.DateTimeField(auto_now_add=True)

    num_score = zip(range(1, 11), range(1, 11))
    score = models.IntegerField(choices=num_score)


class Comment(models.Model):
    """
        Information from the comments
        """
    text = models.TextField(max_length=200)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name="comments")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return str(self.pk)
