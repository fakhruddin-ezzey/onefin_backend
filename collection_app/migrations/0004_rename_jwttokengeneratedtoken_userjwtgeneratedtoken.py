# Generated by Django 4.1.7 on 2023-10-09 18:06

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection_app', '0003_jwttokengeneratedtoken'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JWTTokenGeneratedToken',
            new_name='UserJWTGeneratedToken',
        ),
    ]
