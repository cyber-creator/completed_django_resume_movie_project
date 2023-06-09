# Generated by Django 3.1.7 on 2021-09-14 00:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('films', '0015_auto_20210825_2249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-posted_date',), 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AddField(
            model_name='comment',
            name='dislike',
            field=models.ManyToManyField(blank=True, related_name='comments_dislike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comments_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
