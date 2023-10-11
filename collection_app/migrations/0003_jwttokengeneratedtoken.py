# Generated by Django 4.1.7 on 2023-10-09 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection_app', '0002_usercollectionmovies_created_on_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JWTTokenGeneratedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(default='')),
                ('refresh_token', models.TextField(default='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated_on', models.DateTimeField(auto_now=True)),
                ('user_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_jwt_generated_token',
            },
        ),
    ]
