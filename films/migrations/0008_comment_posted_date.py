# Generated by Django 3.1.7 on 2021-07-08 21:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_auto_20210706_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='posted_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]