from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    last_name = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    profile_img = models.ImageField(default='default_profile.png', upload_to='profile_avatar')

    def __str__(self):
        return f'{self.user.username} profile'
