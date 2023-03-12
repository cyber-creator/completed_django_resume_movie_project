from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('filter/', views.filter_films, name='filter_films'),
    path('<slug:category_slug>', views.film_list_category, name='films_catalog_category'),
    path('genre/<int:pk>/<str:slug>', views.film_list_genre, name='films_catalog_genre'),
    path('review/<slug:film_slug>/', views.add_review_or_comment, name='add_review'),
    path('search-result/', views.search_result, name='search_result'),
    path('film/<slug:film_slug>', views.detail_page, name='detail_page'),
    path('about/', views.about_page, name='about'),
    path('contacts/', views.contact_page, name='contacts'),
    path('privacy/', views.privacy_page, name='privacy_policy'),
    path('delete-comment/<int:pk>/<str:slug>', views.delete_comment, name='delete_comment'),
    path('delete_review/<int:pk>/<str:slug>', views.delete_review, name='delete_review'),
    path('like_comment/', views.comments_likes_or_dislike, name='like_unlike_comment'),
    path('like_review/', views.review_likes_or_dislike, name='like_unlike_review'),
    path('selected/', views.selected_movie, name='selected_movie'),
]
