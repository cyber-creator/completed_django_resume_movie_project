from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register('category', views.CategoryAPIViewSets, basename='category')
router.register('genre', views.GenreAPIViewSets, basename='genre')
router.register('stills', views.StillsAPIViewSets, basename='stills')
router.register('review', views.ReviewAPIViewSets, basename='review')
router.register('', views.FilmsAPIViewSets, basename='movie')


urlpatterns = router.urls
