# Generated by Django 4.1.7 on 2023-10-10 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection_app', '0008_alter_usercollectionmovies_collection_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercollectionmovies',
            name='collection_map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection_app.usercollections'),
        ),
    ]
