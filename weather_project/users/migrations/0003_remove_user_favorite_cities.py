# Generated by Django 5.0.6 on 2024-06-08 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_favorite_cities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favorite_cities',
        ),
    ]