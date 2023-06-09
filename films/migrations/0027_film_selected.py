# Generated by Django 3.1.7 on 2022-03-12 07:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('films', '0026_auto_20220311_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='selected',
            field=models.ManyToManyField(blank=True, related_name='movies_selected', to=settings.AUTH_USER_MODEL),
        ),
    ]
