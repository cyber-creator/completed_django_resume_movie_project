from django.contrib.auth import get_user_model
from rest_framework import serializers
from films.models import Category, Genre, Film, Review, Stills


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'film', 'rating', 'title', 'author', 'review', 'created')


class StillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stills
        fields = ('id', 'title', 'stills', 'films')


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('title', 'poster', 'genre', 'category', 'plot', 'release_year', 'running_time', 'country', 'actors',
                  'directors', 'slug', 'date_added', 'editor_choice', 'available', 'video', 'selected', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')
