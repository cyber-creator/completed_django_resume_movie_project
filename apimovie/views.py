from django.shortcuts import render
from rest_framework import generics, permissions
# from django.contrib.auth import get_user_model
from rest_framework import viewsets
from apimovie.permissions import IsHaveAccountPerm
from apimovie.serializers import FilmSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, StillsSerializer
from films.models import Film, Category, Genre, Stills, Review


class ReviewAPIViewSets(viewsets.ModelViewSet):
    permission_classes = (IsHaveAccountPerm,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class StillsAPIViewSets(viewsets.ModelViewSet):
    permission_classes = (IsHaveAccountPerm,)
    queryset = Stills.objects.all()
    serializer_class = StillsSerializer


class FilmsAPIViewSets(viewsets.ModelViewSet):
    permission_classes = (IsHaveAccountPerm,)
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class CategoryAPIViewSets(viewsets.ModelViewSet):
    permission_classes = (IsHaveAccountPerm,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreAPIViewSets(viewsets.ModelViewSet):
    permission_classes = (IsHaveAccountPerm,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
#
#
# class UsersAPIViewsSets(viewsets.ModelViewSet):
#     queryset = get_user_model().objects.all()
#     serializer_class = UsersSerializer
