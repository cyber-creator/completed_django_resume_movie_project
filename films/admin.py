from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'poster', 'category',
                    'release_year', 'running_time', 'country', 'slug', 'get_average_rating')
    list_filter = ('category', 'genre')
    list_editable = ('category', 'country', 'release_year')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Stills)
class StillsAdmin(admin.ModelAdmin):
    list_display = ('title', 'films')
    list_filter = ('title', 'films')


admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Actors)
admin.site.register(Review)
admin.site.register(Contact)

