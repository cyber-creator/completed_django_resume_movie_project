# Generated by Django 3.1.7 on 2022-05-22 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220318_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='default_profile.png', upload_to='profile_avatar'),
        ),
    ]