# Generated by Django 3.1.7 on 2022-01-11 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0023_auto_20220110_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('text', models.TextField()),
            ],
        ),
    ]
