from django.contrib import admin
from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_name', 'phone_number', 'profile_img']
