# Generated by Django 4.1.7 on 2023-10-09 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCollections',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(default='N/A')),
                ('user_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_movies_collection',
            },
        ),
        migrations.CreateModel(
            name='UserCollectionMovies',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(default='N/A')),
                ('genres', models.CharField(max_length=200)),
                ('collection_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection_app.usercollections')),
            ],
            options={
                'db_table': 'user_movies_collection_specific',
            },
        ),
    ]
