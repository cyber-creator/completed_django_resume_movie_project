# Generated by Django 3.1.7 on 2021-10-04 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0019_auto_20211004_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='video',
            field=models.FileField(default='video/unavailable.mp4', upload_to='video/', verbose_name='video'),
        ),
    ]
